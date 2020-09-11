import * as React from 'react';
import { createStackNavigator } from '@react-navigation/stack';

import ViewProfile from '../../../screens/view_profile';
import FriendsList from '../../../screens/friends_list';

const Stack = createStackNavigator();

export default function NavigationStack() {
  return (
    <Stack.Navigator>
        <Stack.Screen name="main" component={FriendsList} />
        <Stack.Screen name="profile" component={ViewProfile} />
    </Stack.Navigator>
  );
}