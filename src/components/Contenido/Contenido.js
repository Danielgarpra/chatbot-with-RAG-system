import React, { Component } from 'react';
import Chatbot from 'react-chatbot-kit';
import { ThemeProvider } from 'styled-components';
import config from '../../config/config';
import MessageParser from '../../config/MessageParser';
import ActionProvider from '../../config/ActionProvider';

const theme = {
    background: '#f5f8fb',
    header: '#5856d6',
    botBubbleColor: '#376B7E',
    userBubbleColor: '#000000',
    botTextColor: '#ffffff',
};


export default class Contenido extends Component {
    render() {
        return (
            <ThemeProvider theme={theme}>
                <Chatbot
                    config={config}
                    messageParser={MessageParser}
                    actionProvider={ActionProvider}
                />
            </ThemeProvider>
        )
    }
}
