
module App exposing (main)


-- IMPORTS
import Messages exposing (Msg(..))

-- import Json.Encode as Encode
import Html exposing (Html, div, p, text, program, input)
import Html.Attributes exposing (class, type_, property)

import Layout.Components exposing ( applicationView
                                  , frame
                                  , box
                                  , BoxColor( BlueBox
                                            , GreyBox
                                            )
                                  )


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
        Noop -> (model, Cmd.none)


-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none

