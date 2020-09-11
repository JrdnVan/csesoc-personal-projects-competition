import React, { Component } from 'react';
import Navigation from "./src/navigation/root_navigate";
import BottomTab from "./src/navigation/main_bottom_tab";
import { NavigationContainer } from '@react-navigation/native';

export default function App() {
        return(
        <NavigationContainer>
            <Navigation/>
        </NavigationContainer>
    );
}
