import * as React from 'react';
import { createStackNavigator } from '@react-navigation/stack';

import ViewProfile from '../../../screens/view_profile';
import ViewEvents from '../../../screens/view_events';
import Event from '../../../screens/event';

const Stack = createStackNavigator();

export default function NavigationStack() {
  return (
    <Stack.Navigator>
        <Stack.Screen name="main" component={ViewEvents} />
        <Stack.Screen name="event" component={Event} />
        <Stack.Screen name="profile" component={ViewProfile} />
    </Stack.Navigator>
  );
}