
module App exposing (main)


-- IMPORTS
import Messages exposing (Msg(..))
import Html exposing (Html, div, p, text, program)

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

-- VIEW
view : Model -> Html Msg
view model =
    applicationView [ div []
                          [ p [] [text "test"]
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

