import { createStackNavigator } from 'react-navigation-stack';
import { NavigationContainer } from '@react-navigation/native';
import * as React from 'react';

import ViewProfile from '../../screens/view_profile';
import ViewEvents from '../../screens/view_events'; 
import EventCard from "../../components/event_card";
  
const Stack = createStackNavigator();

function ProfileStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen name="Cards" component={ViewEvents} />
            <Stack.Screen name="Profile" component={ViewProfile} />
            <Stack.Screen name="Event" component={ViewProfile} />
        </Stack.Navigator>
    )
}

export default function ProfileStackNavigator() {
    return (
        <NavigationContainer>
            <ProfileStack/>
        </NavigationContainer>
    );
}