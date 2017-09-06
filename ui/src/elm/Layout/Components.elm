
module Layout.Components exposing (applicationView)

-- IMPORTS
import Html exposing (Html, div, p, h1, text)
import Html.Attributes exposing (class)


import Messages exposing (Msg)


applicationView : List (Html Msg) -> Html Msg
applicationView mainView =
   div [class "app-container"]
       [ header
       , div [class "app-main"] mainView
       , footer
       ]
                                   
header : Html msg
header =
    div [class "app-header"]
        [h1 [class "navbar navbar-fixed-top navbar-inverse"]
            [text "Denon Pro"]]


footer : Html msg
footer =
    div [class "app-footer"]
        [div [class "footer-text"]  
             [p [class "pull-left"]
                [text "(c) 1993 Computer Club Chaos Systems Inc." ]
             ,p [class "pull-right text-warning"] [text "Unlicensed Copy"]
             ]]






