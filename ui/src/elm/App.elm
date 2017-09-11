
module App exposing (main)


-- IMPORTS
import Messages exposing ( Msg(..)
                         , getMatrixConfigs
                         )
import Model exposing ( Model
                      , AmpState
                      , AudioMatrixConfig
                      , AudioMatrixUploadState
                      , MasterVolume
                      , initialModel
                      )

-- import Json.Encode as Encode
import RemoteData exposing (WebData)
import Html exposing (Html, div, p, text, program, input)
import Html.Attributes exposing (class, type_, property)

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
init = (initialModel, getMatrixConfigs)



-- TEST

viewStatus : Html Msg
viewStatus =
    div [class "amp-status"]
        [ masterVolume
        ]



masterVolume : Html Msg
masterVolume =
    div [ class "master-volume-ctrl" ]
        [ text "Master Volume"
        ]


infoBox : Html Msg
infoBox =
    frame Nothing
          BlueBox
          [ p [] [text "Today Is Prickel Prickle"]
          , p [] [text "23:42:42 @ 2017-23-42" ]
          ]

fooBox : Html Msg
fooBox =
    frame (Just "Master Volume")
    GreyBox
    [ p [] [text "23.5%"] ]
    



-- VIEW
view : Model -> Html Msg
view model =
    applicationView (Just [ div []
                                [text "Left sidebar"]
                          ])
                    [ div []
                          [ masterVolume
                          ]
                    ]
                    (Just [ div []
                                [ infoBox
                                , fooBox
                                ]

                          ]) 

-- UPDATE
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        -- Do nothing
        Nop -> (model, Cmd.none)

        -- Current Time
        Tick time -> ({model | now = time}, Cmd.none)
    
        -- RemoteData
        AmpStateResponse state            -> updateAmpState model state
        UploadStateResponse state         -> updateUploadState model state
        MasterVolumeResponse masterVolume -> updateMasterVolume model masterVolume
        MatrixConfigsListResponse configs -> updateMatrixConfigsList model configs 



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
    in 
        ({model | amp = next}, Cmd.none)


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
    Sub.none

