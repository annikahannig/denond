
module App exposing (main)


-- IMPORTS
import Messages exposing (Msg(..))

import Json.Encode as Encode
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
    div []
        [ input [ type_ "range"
                , property "min"  (Encode.int 0)
                , property "max"  (Encode.int 100)
                , property "step" (Encode.float 0.5)
                , class "range-select"
                ]
                []
         ]



-- VIEW
view : Model -> Html Msg
view model =
    applicationView [ div []
                          [ masterVolume
                          ]
                    ]

-- UPDATE
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        Noop -> (model, Cmd.none)


-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none

