
module App exposing (main)


-- IMPORTS
import Messages exposing (Msg(..))

-- import Json.Encode as Encode
import Html exposing (Html, div, p, text, program, input)
import Html.Attributes exposing (class, type_, property)

import Layout.Components exposing (applicationView)


type alias Model = 
    { foo : Int
    }


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
init =
    ( Model 0
    , Cmd.none
    )



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
                                [text "Right sidebar"]
                          ]) 

-- UPDATE
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        Noop -> (model, Cmd.none)


-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none

