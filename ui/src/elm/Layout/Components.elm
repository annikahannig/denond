
module Layout.Components exposing (applicationView)

-- IMPORTS
import Html exposing (Html, div, p, h1, text)
import Html.Attributes exposing (class)


import Messages exposing (Msg)


{- Base Layout -}


applicationView :  Maybe (List (Html Msg)) 
                -> List (Html Msg) 
                -> Maybe (List (Html Msg))
                -> Html Msg
applicationView leftView mainView rightView =
    let
        -- The main content zones are
        --   Left |      Main      | Right
        -- These are wrapped within the app-main flexbox
        left = case leftView of
            Just view -> [ div [class "content-left"] view ]
            Nothing   -> []

        right = case rightView of
            Just view -> [ div [class "content-right"] view ]
            Nothing   -> []

        main = [ div [class "content-main"] mainView ]
    in 
        div [class "app-container"]
            [ header
            , div [class "app-main"] (left ++ main ++ right)
            , footer
            ]
                                   
header : Html Msg 
header =
    div [class "app-header"]
        [h1 [class "navbar navbar-fixed-top navbar-inverse"]
            [text "Denon Pro"]]


footer : Html Msg 
footer =
    div [class "app-footer"]
        [div [ class "footer-text" ]  
             [ p [class "pull-left"]
                 [text "(c) 1993 Computer Club Chaos Systems Inc." ]
             , p [class "pull-right text-warning"]
                 [text "Unlicensed Copy"]
             ]]




{- Helper Components, like frames, boxes and so on -}







