
module Messages exposing ( Msg(..)
                         , getMasterVolume
                         , setMasterVolume
                         , getMatrixConfigs
                         )

import Debug

import Http
import Json.Decode as Decode exposing (Decoder)
import Json.Encode as Encode exposing (encode, object)
import Json.Decode.Pipeline exposing (decode, required, requiredAt)
import Time exposing (Time)

import RemoteData exposing (RemoteData, WebData)

import Model exposing ( AmpState
                      , AudioMatrixConfig
                      , AudioMatrixUploadState
                      , MasterVolume
                      )

type Msg
    = Nop
    | Tick Time
    | AmpStateResponse (WebData AmpState)
    | MasterVolumeResponse (WebData MasterVolume)
    | UploadStateResponse (WebData AudioMatrixUploadState)
    | MatrixConfigsListResponse (WebData (List AudioMatrixConfig))
  

-- API

getAmpState : Cmd Msg
getAmpState =
    let
        endpoint = "/api/mainzone/state"
    in
        Http.get endpoint ampStateDecoder
            |> RemoteData.sendRequest
            |> Cmd.map AmpStateResponse



getMasterVolume : Cmd Msg
getMasterVolume =
    let endpoint = "/api/volume/master"
    in
        Http.get endpoint masterVolumeDecoder
            |> RemoteData.sendRequest
            |> Cmd.map MasterVolumeResponse 


setMasterVolume : Float -> Cmd Msg
setMasterVolume volume = 
    let
        endpoint = "/api/volume/master"
        body = Http.stringBody "application/json"
                               (encodeMasterVolume volume)
    in
        Http.post endpoint body masterVolumeDecoder
            |> RemoteData.sendRequest
            |> Cmd.map MasterVolumeResponse


getMatrixConfigs : Cmd Msg
getMatrixConfigs =
    let endpoint = "/api/matrix-config/configs"
    in
        Http.get endpoint apiConfigsDecoder
            |> RemoteData.sendRequest
            |> Cmd.map MatrixConfigsListResponse



setMatrixConfig : Int -> Cmd Msg
setMatrixConfig =
    let endpoint = "/api/matrix-config/configs"
    in
        Http.post endpoint body uploadStateDecoder
            |> RemoteData.sendRequest
            |> Cmd.map MatrixConfigUploadStateResponse


-- DECODERS / ENCODERS

ampStateDecoder : Decoder AmpState
ampStateDecoder =
    decode AmpState
        |> requiredAt ["state", "on"]     Decode.bool
        |> requiredAt ["state", "source"] Decode.string


masterVolumeDecoder : Decoder MasterVolume
masterVolumeDecoder =
    decode MasterVolume
        |> requiredAt ["volume", "master"] Decode.float


encodeMasterVolume : Float -> String 
encodeMasterVolume volume =
    encode 0
        ( object
            [ ("volume", Encode.float volume) ]
        ) 


apiConfigsDecoder : Decoder (List AudioMatrixConfig)
apiConfigsDecoder =
    Decode.at ["configs"]
              (Decode.list audioMatrixConfigDecoder)
        
audioMatrixConfigDecoder : Decoder AudioMatrixConfig
audioMatrixConfigDecoder =
    decode AudioMatrixConfig
        |> required "id" Decode.int
        |> required "name" Decode.string
        |> required "selected" Decode.bool

uploadStateDecoder : Decoder UploadState

