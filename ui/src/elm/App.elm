
module App exposing (main)


-- IMPORTS
import Messages exposing ( Msg(..)
                         , getMatrixConfigs
                         , setMatrixConfig
                         , getMasterVolume
                         , getUploadState
                         )
import Model exposing ( Model
                      , AmpState
                      , AudioMatrixConfig
                      , AudioMatrixUploadState
                      , MasterVolume
                      , initialModel
                      )

-- import Json.Encode as Encode
import Task
import Time exposing (Time)
import Date exposing (Date)
import RemoteData exposing (WebData)
import Html exposing (Html, div, p, text, program, input, button)
import Html.Attributes exposing (class, type_, property)
import Html.Events exposing (onClick)

import Time.Format

import Layout.Components exposing ( applicationView
                                  , frame
                                  , box
                                  , BoxColor( BlueBox
                                            , GreyBox
                                            )
                                  )


-- Main Program
main : Program Never Model Msg
main =
    program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


-- INIT
init : (Model, Cmd Msg)
init = (initialModel, Cmd.batch [ getMatrixConfigs
                                , getMasterVolume
                                , getUploadState
                                , setCurrentTime
                                ])


setCurrentTime : Cmd Msg
setCurrentTime =
    Task.perform Tick Time.now


-- UI
viewStatus : Html Msg
viewStatus =
    div [class "amp-status"]
        [ text "amp status" 
        ]


audioMatrixSelector : Model -> Html Msg
audioMatrixSelector model =
    let
        isSelected selected =
            if selected then " (selected)"
                        else ""

        matrixView audioMatrix =
            div [ class "audio-matrix" ]
                [ button [ class "btn btn-matrix-select"
                         , onClick (SetAudioMatrix audioMatrix.id)
                         ]
                         [ text ((toString audioMatrix.id) 
                                 ++ ": "
                                 ++ (toString audioMatrix.name)
                                 ++ (isSelected audioMatrix.isSelected))
                         ]
                ]
    
        grid configs =
            div [ class "audio-matrix-grid" ]
                (List.map matrixView configs)

        selector configs =
            case configs of
                RemoteData.NotAsked      -> text "Initializing..."
                RemoteData.Loading       -> text "Loading..."
                RemoteData.Failure err   -> text (toString err)
                RemoteData.Success all   -> grid all
   
        updateView = [ p [] [text "Updating AudioMatrix..."]
                     , p [] [text "This may take a while."]
                     ]


        uploadSwitch uploadState updating idle =
            case uploadState of
                RemoteData.NotAsked      -> idle
                RemoteData.Loading       -> idle
                RemoteData.Failure _     -> idle
                RemoteData.Success state ->
                    if state.isUploading then updating
                                         else idle

    in
        frame (Just "Select AudioMatrix")
              BlueBox
              (uploadSwitch model.amp.uploadState
                            updateView
                            [selector model.amp.matrixConfigs])



masterVolumeView : Model -> Html Msg
masterVolumeView model =
    let 
        volumeView data = case data of
            RemoteData.Success vol ->
                div [ class "master-volume-ctrl" ]
                    [ p [] [text "Master Volume:"]
                    , p [] [text ((toString vol.value) ++ "%")]
                    ]
            RemoteData.NotAsked    -> div [] [text "Loading..."]
            RemoteData.Loading     -> div [] [text "Loading..."]
            RemoteData.Failure err -> div [ class "error" ]
                                          [ text (toString err) ]

    in
        frame Nothing
              GreyBox 
              [ volumeView model.amp.masterVolume ]


infoBox : Model -> Html Msg
infoBox model =
    frame Nothing
          BlueBox 
          [ p [] [text (formatTime model.now)]
          ]


formatTime : Time -> String
formatTime t =
    Time.Format.format "%a %b %d %H:%M:%S %Y" t


fooBox : Html Msg
fooBox =
    frame (Just "Master Volume")
    GreyBox
    [ p [] [text "23.5%"] ]
    



-- VIEW
view : Model -> Html Msg
view model =
    applicationView (Just [ div []
                                [ audioMatrixSelector model ]
                          ])
                    [ div []
                          [ 
                          ]
                    ]
                    (Just [ div []
                                [ infoBox model
                                , masterVolumeView model 
                                ]

                          ]) 

-- UPDATE
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        -- Do nothing
        Nop -> (model, Cmd.none)

        -- Current Time
        Tick time -> updateTime model time 

        -- Events
        SetAudioMatrix id -> setAudioMatrix model id
    
        -- RemoteData
        AmpStateResponse state            -> updateAmpState model state
        UploadStateResponse state         -> updateUploadState model state
        MasterVolumeResponse masterVolume -> updateMasterVolume model masterVolume
        MatrixConfigsListResponse configs -> updateMatrixConfigsList model configs 



updateTime : Model -> Time -> (Model, Cmd Msg)
updateTime model t =
    -- Handle periodic tasks
    let 
        cmd = if ((truncate t) % 3 == 0) then
                    if model.pollUploadState then getUploadState
                                             else Cmd.none
              else Cmd.none

        nextModel = {model | now = t}
    in
        (nextModel, cmd)



setAudioMatrix : Model -> Int -> (Model, Cmd Msg)
setAudioMatrix model id =
    ( {model | pollUploadState = True}
    , setMatrixConfig id
    )


updateAmpState : Model -> WebData AmpState -> (Model, Cmd Msg)
updateAmpState model nextState =
    let
        amp = model.amp
        nextAmp = {amp | state = nextState }
    in
        ({model | amp = nextAmp}, Cmd.none)


updateUploadState : Model -> WebData AudioMatrixUploadState -> (Model, Cmd Msg)
updateUploadState model state =
    let
        amp = model.amp
        next = {amp | uploadState = state}
        pollState = case state of
            RemoteData.Success s -> s.isUploading
            RemoteData.Failure _ -> False
            RemoteData.NotAsked  -> False
            RemoteData.Loading   -> False
    in 
        ({model | amp = next, pollUploadState = pollState}, Cmd.none)


updateMasterVolume : Model -> WebData MasterVolume -> (Model, Cmd Msg)
updateMasterVolume model volume =
    let
        amp = model.amp
        next = {amp | masterVolume = volume}
    in
        ({model | amp = next}, Cmd.none)


updateMatrixConfigsList : Model -> WebData (List AudioMatrixConfig)
                                -> (Model, Cmd Msg)
updateMatrixConfigsList model configs =
    let
        amp = model.amp
        next = {amp | matrixConfigs = configs}
    in
        ({model | amp = next}, Cmd.none)



-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
    Time.every Time.second Tick

