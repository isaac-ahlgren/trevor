

#include <stdio.h>
#include <stdlib.h>
#include "portaudio.h"
#include <string.h>

#define NUM_CHANNELS 1
#define SAMPLE_SILENCE  (0.0f)
#define SAMPLE_RATE  (44100)
#define NUM_SECONDS 5
#define FRAMES_PER_BUFFER (512)
#define PA_SAMPLE_TYPE  paFloat32 
typedef float SAMPLE;


typedef struct
{       
    int          frameIndex;  /* Index into sample array. */
    int          maxFrameIndex;
    SAMPLE      *recordedSamples;
}       
paTestData; 

/* This routine will be called by the PortAudio engine when audio is needed.
** It may be called at interrupt level on some machines so don't do anything
** that could mess up the system like calling malloc() or free().
*/
static int recordCallback( const void *inputBuffer, void *outputBuffer,
                           unsigned long framesPerBuffer,
                           const PaStreamCallbackTimeInfo* timeInfo,
                           PaStreamCallbackFlags statusFlags,
                           void *userData )
{
    paTestData *data = (paTestData*)userData;
    const SAMPLE *rptr = (const SAMPLE*)inputBuffer;
    SAMPLE *wptr = &data->recordedSamples[data->frameIndex * NUM_CHANNELS];
    long framesToCalc;
    long i;
    int finished;
    unsigned long framesLeft = data->maxFrameIndex - data->frameIndex;

    (void) outputBuffer; /* Prevent unused variable warnings. */
    (void) timeInfo;
    (void) statusFlags;
    (void) userData;

    if( framesLeft < framesPerBuffer )
    {
        framesToCalc = framesLeft;
        finished = paComplete;
    }
    else
    {
        framesToCalc = framesPerBuffer;
        finished = paContinue;
    }

    if( inputBuffer == NULL )
    {
        for( i=0; i<framesToCalc; i++ )
        {
            *wptr++ = SAMPLE_SILENCE;  /* left */
            if( NUM_CHANNELS == 2 ) *wptr++ = SAMPLE_SILENCE;  /* right */
        }
    }
    else
    {
        for( i=0; i<framesToCalc; i++ )
        {
            *wptr++ = *rptr++;  /* left */
            if( NUM_CHANNELS == 2 ) *wptr++ = *rptr++;  /* right */
        }
    }
    data->frameIndex += framesToCalc;
    return finished;
}


/* This routine will be called by the PortAudio engine when audio is needed.
** It may be called at interrupt level on some machines so don't do anything
** that could mess up the system like calling malloc() or free().
*/
static int playCallback( const void *inputBuffer, void *outputBuffer,
                         unsigned long framesPerBuffer,
                         const PaStreamCallbackTimeInfo* timeInfo,
                         PaStreamCallbackFlags statusFlags,
                         void *userData )
{
    paTestData *data = (paTestData*)userData;
    SAMPLE *rptr = &data->recordedSamples[data->frameIndex * NUM_CHANNELS];
    SAMPLE *wptr = (SAMPLE*)outputBuffer;
    unsigned int i;
    int finished;
    unsigned int framesLeft = data->maxFrameIndex - data->frameIndex;

    (void) inputBuffer; /* Prevent unused variable warnings. */
    (void) timeInfo;
    (void) statusFlags;
    (void) userData;

    if( framesLeft < framesPerBuffer )
    {
        /* final buffer... */
        for( i=0; i<framesLeft; i++ )
        {
            *wptr++ = *rptr++;  /* left */
            if( NUM_CHANNELS == 2 ) *wptr++ = *rptr++;  /* right */
        }
        for( ; i<framesPerBuffer; i++ )
        {
            *wptr++ = 0;  /* left */
            if( NUM_CHANNELS == 2 ) *wptr++ = 0;  /* right */
        }
        data->frameIndex += framesLeft;
        finished = paComplete;
    }
    else
    {
        for( i=0; i<framesPerBuffer; i++ )
        {
            *wptr++ = *rptr++;  /* left */
            if( NUM_CHANNELS == 2 ) *wptr++ = *rptr++;  /* right */
        }
        data->frameIndex += framesPerBuffer;
        finished = paContinue;
    }
    return finished;
}

void playback(PaStream *playData) {
    PaStream *OutputStream;
    int err;
    PaStreamParameters  outputParameters;
    outputParameters.device = Pa_GetDefaultOutputDevice(); /* default output device */
    if (outputParameters.device == paNoDevice) {
        fprintf(stderr,"Error: No default output device.\n");
        exit(1);
    }
    outputParameters.channelCount = 1;                     /* stereo output */
    outputParameters.sampleFormat =  PA_SAMPLE_TYPE;
    outputParameters.suggestedLatency = Pa_GetDeviceInfo( outputParameters.device )->defaultLowOutputLatency;
    outputParameters.hostApiSpecificStreamInfo = NULL;


    err = Pa_OpenStream(
              &OutputStream,
              NULL, /* no input */
              &outputParameters,
              SAMPLE_RATE,
              FRAMES_PER_BUFFER,
              paClipOff,      /* we won't output out of range samples so don't bother clipping them */
              playCallback,
              playData );
    if( err != paNoError ) {
        fprintf(stderr, "ERROR: couldn't open output stream\n");
        fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        exit(1);
    }

    if( OutputStream )
    {
        err = Pa_StartStream( OutputStream );
        if( err != paNoError ) {
            fprintf(stderr, "ERROR: couldn't start output stream\n");
            fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        }
        
        printf("Waiting for playback to finish.\n"); fflush(stdout);

        while( ( err = Pa_IsStreamActive( OutputStream ) ) == 1 ) Pa_Sleep(100);
        if( err < 0 ) {
            fprintf(stderr, "ERROR: couldn't check if stream active\n");
            fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        }
        
        err = Pa_CloseStream( OutputStream );
        if( err != paNoError ) {
            fprintf(stderr, "ERROR: Couldn't close output stream\n");
            fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        }
    }
}

int blocking_sample_audio() {

    int k;
    int err;
    int totalFrames, numSamples, numBytes;
    PaStream *iPhoneStream, *MacbookStream, *OutputStream;
    paTestData          iPhoneData, MacbookData;
    PaStreamParameters  iPhoneInputParameters, MacbookInputParameters, outputParameters;

    totalFrames =  NUM_SECONDS * SAMPLE_RATE;
    numSamples = totalFrames * NUM_CHANNELS;
    numBytes = numSamples * sizeof(SAMPLE);

    iPhoneData.maxFrameIndex = NUM_SECONDS * SAMPLE_RATE;
    iPhoneData.frameIndex = 0;
    iPhoneData.recordedSamples = (SAMPLE *) malloc( numBytes ); /* From now on, recordedSamples is initialised. */

    MacbookData.maxFrameIndex = NUM_SECONDS * SAMPLE_RATE;
    MacbookData.frameIndex = 0;
    MacbookData.recordedSamples = (SAMPLE *) malloc( numBytes ); /* From now on, recordedSamples is initialised. */

    err = Pa_Initialize(); 
    if( err < 0 ) {
        fprintf(stderr, "ERROR: Could not initialize portaudio\n");
        fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        exit(1);
    }

    MacbookInputParameters.device = -1;
    iPhoneInputParameters.device = -1;
    for(k = 0; k < Pa_GetDeviceCount(); k++ ) {
        const PaDeviceInfo* devinfo = Pa_GetDeviceInfo(k);
        if(devinfo == NULL) {
            break;
        }
        fprintf(stderr, "Device %d name     %s  ", k, devinfo->name);
        if(strstr(devinfo->name, "iPhone") != NULL ) {
            printf("FOUND IPHONE!!\n");
            iPhoneInputParameters.device = k;
        } else if(strstr(devinfo->name, "MacBook Pro Microphone") != NULL) {
            printf("FOUND MACBOOK SPEAKERS\n");
            MacbookInputParameters.device = k;
        } else {
            printf("\n");
        }
    }

    if(iPhoneInputParameters.device == -1) {
        fprintf(stderr, "ERROR: Failed to find iPhone audio device\n");
        exit (-1);
    }
    if( MacbookInputParameters.device == -1) {
        fprintf(stderr, "ERROR: Failed to find Macbook audio input device\n");
        exit(-1);
    }


    iPhoneInputParameters.channelCount = 1;                    /* mono input */
    iPhoneInputParameters.sampleFormat = PA_SAMPLE_TYPE;
    iPhoneInputParameters.suggestedLatency = Pa_GetDeviceInfo( iPhoneInputParameters.device )->defaultLowInputLatency;
    iPhoneInputParameters.hostApiSpecificStreamInfo = NULL;

    MacbookInputParameters.channelCount = 1;                    /* mono input */
    MacbookInputParameters.sampleFormat = PA_SAMPLE_TYPE;
    MacbookInputParameters.suggestedLatency = Pa_GetDeviceInfo( MacbookInputParameters.device )->defaultLowInputLatency;
    MacbookInputParameters.hostApiSpecificStreamInfo = NULL;


    /* Record some audio. -------------------------------------------- */
    err = Pa_OpenStream(
              &iPhoneStream,
              &iPhoneInputParameters,
              NULL,                  /* &outputParameters, */
              SAMPLE_RATE,
              FRAMES_PER_BUFFER,
              paClipOff,      /* we won't output out of range samples so don't bother clipping them */
              recordCallback,
              &iPhoneData );
    if( err != paNoError ) {
        fprintf(stderr, "ERROR: Could not open iPhone input stream\n");
        fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        exit(1);
    }
    err = Pa_OpenStream(
              &MacbookStream,
              &MacbookInputParameters,
              NULL,                  /* &outputParameters, */
              SAMPLE_RATE,
              FRAMES_PER_BUFFER,
              paClipOff,      /* we won't output out of range samples so don't bother clipping them */
              recordCallback,
              &MacbookData );
    if( err != paNoError ) {
        fprintf(stderr, "ERROR: Could not open Macbook input stream\n");
        fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        exit(1);
    }

    err = Pa_StartStream( iPhoneStream );
    if( err != paNoError ) {
        fprintf(stderr, "ERROR: Could not start iPhone input stream\n");
        fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        exit(1);
    }


    err = Pa_StartStream( MacbookStream );
    if( err != paNoError ) {
        fprintf(stderr, "ERROR: Could not start Macbook input stream\n");
        fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        exit(1);
    }

    printf("\n=== Now recording!! Please speak into the microphone. ===\n"); fflush(stdout);

    while( ( err = Pa_IsStreamActive( iPhoneStream ) ) == 1 )
    {
        Pa_Sleep(1000);
        printf("Iphone index = %d\n", iPhoneData.frameIndex ); fflush(stdout);
    }
    if( err != paNoError ) {
        fprintf(stderr, "ERROR: Pa_IsStreamActive\n");
        fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        exit(1);
    }



    err = Pa_CloseStream( MacbookStream );
    if( err != paNoError ) {
        fprintf(stderr, "ERROR: Could not close Macbook input stream\n");
        fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        exit(1);
    }
    err = Pa_CloseStream( iPhoneStream );
    if( err != paNoError ) {
        fprintf(stderr, "ERROR: Could not close iPhone input stream\n");
        fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
        exit(1);
    }


    FILE *OutFile = fopen("iphone.txt", "w");
    for(k = 0; k < numSamples; k++) {
      fprintf(OutFile, "%f\n", iPhoneData.recordedSamples[k]);
    }
    fclose(OutFile);
    OutFile = fopen("macbook.txt", "w");
    for(k = 0; k < numSamples; k++) {
      fprintf(OutFile, "%f\n", MacbookData.recordedSamples[k]);
    }
    fclose(OutFile);


    

    /* Playback recorded data.  -------------------------------------------- */
    iPhoneData.frameIndex = 0;
    MacbookData.frameIndex = 0;

    Pa_Sleep(3000);


    printf("\n=== Now playing back iPhone Data ===\n"); fflush(stdout);

    playback(&iPhoneData);
    printf("\n=== Now playing back Macbook Data ===\n"); fflush(stdout);

    playback(&MacbookData);
    printf("Done.\n"); fflush(stdout);
}

