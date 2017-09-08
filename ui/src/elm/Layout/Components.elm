
module Layout.Components exposing ( BoxColor(..)
                                  , applicationView
                                  , box
                                  , frame
                                  )

-- IMPORTS
import Html exposing (Html, div, p, span, h1, text)
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
                 [text "(c) 1993 Computer Club Chaos System GmbH" ]
             , p [class "pull-right text-warning"]
                 [text "Unlicensed Copy"]
             ]]




{- Helper Components, like frames, boxes and so on -}

type BoxColor = BlueBox
              | GreyBox



box : BoxColor -> List (Html Msg) -> Html Msg
box color content =
    let
        cssClass = case color of
            BlueBox -> "box box-blue"
            GreyBox -> "box box-grey"
    in
        div [ class cssClass ] content



frame :  Maybe String 
      -> BoxColor 
      -> List (Html Msg)
      -> Html Msg
frame title color content =
    let
        frameTitle = case title of
            Just t  -> [div [ class "frame-title"] 
                            [ span [] [text t]
                            ]
                       ]
            Nothing -> []

    in
        box color 
            [ div [ class "frame" ]
                  (  frameTitle 
                  ++ [div [ class "frame-content" ] content]
                  )
            ]



