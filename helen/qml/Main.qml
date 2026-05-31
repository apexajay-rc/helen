import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    width: 1120
    height: 760
    minimumWidth: 900
    minimumHeight: 650
    visible: true
    title: "Helen | Desktop Accessibility Copilot"
    color: palette.background

    property bool highContrast: false
    property bool reducedMotion: false
    property color accent: {
        if (helen.state === "listening") return "#65B9FF"
        if (helen.state === "processing") return "#F4C95D"
        if (helen.state === "speaking") return "#C993FF"
        if (helen.state === "guide") return "#7FD7C4"
        return "#52D2A0"
    }
    property var palette: ({
        background: highContrast ? "#000000" : "#07111F",
        surface: highContrast ? "#101010" : "#0D1B2D",
        surfaceRaised: highContrast ? "#191919" : "#11273F",
        border: highContrast ? "#FFFFFF" : "#1E3B59",
        text: "#F5F9FF",
        muted: highContrast ? "#FFFFFF" : "#9CB0C7"
    })

    component ActionButton: Button {
        id: control
        required property string accessibleLabel
        Accessible.name: accessibleLabel
        Accessible.description: "Runs the " + accessibleLabel + " action"
        Accessible.role: Accessible.Button
        focusPolicy: Qt.StrongFocus
        font.pixelSize: 15
        padding: 14

        background: Rectangle {
            radius: 6
            color: control.down ? window.accent : palette.surfaceRaised
            border.color: control.activeFocus ? window.accent : palette.border
            border.width: control.activeFocus ? 3 : 1
        }
        contentItem: Text {
            text: control.text
            color: palette.text
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font: control.font
        }
    }

    Rectangle {
        anchors.fill: parent
        color: palette.background

        RowLayout {
            anchors.fill: parent
            anchors.margins: 30
            spacing: 24

            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 12

                Text {
                    text: "HELEN"
                    color: palette.text
                    font.pixelSize: 28
                    font.weight: Font.DemiBold
                    Accessible.name: "Helen desktop accessibility copilot"
                }

                Text {
                    text: "Local-first desktop accessibility copilot"
                    color: palette.muted
                    font.pixelSize: 14
                }

                Item {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 340

                    Repeater {
                        model: 4
                        Rectangle {
                            required property int index
                            anchors.centerIn: parent
                            width: 184 + index * 42
                            height: width
                            radius: width / 2
                            color: "transparent"
                            border.color: Qt.rgba(window.accent.r, window.accent.g, window.accent.b, 0.42 - index * 0.07)
                            border.width: 2
                            scale: 1

                            SequentialAnimation on scale {
                                running: !window.reducedMotion
                                loops: Animation.Infinite
                                NumberAnimation { to: 1.06; duration: 1150 + index * 130; easing.type: Easing.InOutSine }
                                NumberAnimation { to: 1.0; duration: 1150 + index * 130; easing.type: Easing.InOutSine }
                            }
                        }
                    }

                    Rectangle {
                        anchors.centerIn: parent
                        width: 154
                        height: 154
                        radius: 77
                        color: window.accent
                        border.color: "#EAF6FF"
                        border.width: 2

                        SequentialAnimation on scale {
                            running: !window.reducedMotion
                            loops: Animation.Infinite
                            NumberAnimation { to: helen.state === "idle" ? 1.03 : 1.09; duration: 780; easing.type: Easing.InOutSine }
                            NumberAnimation { to: 1.0; duration: 780; easing.type: Easing.InOutSine }
                        }

                        Column {
                            anchors.centerIn: parent
                            spacing: 6
                            Text {
                                anchors.horizontalCenter: parent.horizontalCenter
                                text: "HELEN"
                                color: "#062036"
                                font.pixelSize: 20
                                font.weight: Font.Bold
                            }
                            Text {
                                anchors.horizontalCenter: parent.horizontalCenter
                                text: helen.state.toUpperCase()
                                color: "#173D55"
                                font.pixelSize: 10
                                font.weight: Font.DemiBold
                            }
                        }
                    }
                }

                Text {
                    Layout.fillWidth: true
                    text: helen.state === "idle" ? "Ready" : helen.state.charAt(0).toUpperCase() + helen.state.slice(1)
                    color: window.accent
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: 22
                    font.weight: Font.DemiBold
                    Accessible.name: "Helen status: " + text
                }

                Text {
                    Layout.fillWidth: true
                    Layout.maximumWidth: 720
                    text: helen.message
                    color: palette.muted
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: 15
                    lineHeight: 1.2
                    Accessible.name: text
                }

                RowLayout {
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 9

                    ActionButton {
                        text: "Hear options"
                        accessibleLabel: "Hear options"
                        onClicked: helen.runCommand("help")
                    }
                    ActionButton {
                        text: "Read screen"
                        accessibleLabel: "Read current screen"
                        onClicked: helen.runCommand("read my screen")
                    }
                    ActionButton {
                        text: "Read camera"
                        accessibleLabel: "Read text using camera"
                        onClicked: helen.runCommand("read this label")
                    }
                    ActionButton {
                        text: "Describe"
                        accessibleLabel: "Describe nearby objects"
                        onClicked: helen.runCommand("describe objects")
                    }
                    ActionButton {
                        text: "Music"
                        accessibleLabel: "Start gesture controlled music"
                        onClicked: helen.runCommand("play music")
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    Layout.topMargin: 8
                    spacing: 8

                    TextField {
                        id: commandInput
                        Layout.fillWidth: true
                        placeholderText: "Ask naturally: read my screen, describe what is ahead, search accessibility..."
                        color: palette.text
                        placeholderTextColor: palette.muted
                        font.pixelSize: 15
                        Accessible.name: "Type a request for Helen"
                        Accessible.description: placeholderText
                        Accessible.role: Accessible.EditableText
                        onAccepted: {
                            helen.runCommand(text)
                            clear()
                        }
                        background: Rectangle {
                            radius: 6
                            color: palette.surfaceRaised
                            border.color: commandInput.activeFocus ? window.accent : palette.border
                            border.width: commandInput.activeFocus ? 3 : 1
                        }
                    }

                    ActionButton {
                        text: "Send"
                        accessibleLabel: "Send typed request"
                        onClicked: {
                            helen.runCommand(commandInput.text)
                            commandInput.clear()
                        }
                    }

                    ActionButton {
                        text: helen.busy ? "Working..." : "Start listening"
                        accessibleLabel: "Start listening for a voice request"
                        enabled: !helen.busy
                        onClicked: helen.startListening()
                    }
                }
            }

            Rectangle {
                Layout.preferredWidth: 300
                Layout.fillHeight: true
                radius: 8
                color: palette.surface
                border.color: palette.border
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 18
                    spacing: 12

                    Text {
                        text: "Activity"
                        color: palette.text
                        font.pixelSize: 18
                        font.weight: Font.DemiBold
                    }

                    ListView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        spacing: 8
                        model: helen.history

                        delegate: Rectangle {
                            required property string modelData
                            width: ListView.view.width
                            height: historyText.implicitHeight + 20
                            radius: 5
                            color: palette.surfaceRaised

                            Text {
                                id: historyText
                                anchors.fill: parent
                                anchors.margins: 10
                                text: modelData
                                color: palette.muted
                                wrapMode: Text.WordWrap
                                font.pixelSize: 12
                            }
                        }
                    }

                    CheckBox {
                        text: "High contrast"
                        checked: window.highContrast
                        onToggled: window.highContrast = checked
                        Accessible.name: "Toggle high contrast mode"
                    }

                    CheckBox {
                        text: "Reduced motion"
                        checked: window.reducedMotion
                        onToggled: window.reducedMotion = checked
                        Accessible.name: "Toggle reduced motion mode"
                    }
                }
            }
        }
    }
}
