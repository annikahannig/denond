
module Model exposing ( Model
                      , Amp
                      , AmpState
                      , AudioMatrixConfig
                      , AudioMatrixUploadState
                      , MasterVolume
                      , initialModel
                      )

import Time exposing (Time)

import RemoteData exposing (RemoteData, WebData)


type alias Model =
    { amp : Amp
    , now : Time
    }

initialModel : Model
initialModel =
    Model initialAmp initialTime

initialTime : Time
initialTime = 0



type alias Amp =
    { state : WebData AmpState
    , masterVolume : WebData MasterVolume
    , matrixConfigs : WebData (List AudioMatrixConfig)
    , uploadState : WebData AudioMatrixUploadState
    }

initialAmp : Amp
initialAmp =
    Amp RemoteData.Loading 
        RemoteData.Loading 
        RemoteData.Loading
        RemoteData.Loading


type alias AmpState =
    { powerOn : Bool
    , source : String
    }


type alias MasterVolume = { value : Float }

type alias AudioMatrixConfig =
    { id : Int
    , name : String
    , selected : Bool
    }

type alias AudioMatrixUploadState =
    { isUploading : Bool
    , error : Maybe String
    }

