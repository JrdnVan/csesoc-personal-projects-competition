import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import SCREEN_NAMES from './screen_names';
import ViewEvents from '../../screens/view_events';
import FriendsList from '../../screens/friends_list';
import TrackEvents from '../../screens/track_events';
import CreateEvent from '../../screens/create_event';
import Settings from '../../screens/settings';
import ViewEventsNavigate from './view_events_navigate';
import FriendsListNavigate from './friends_list_navigate';
import React from 'react';

const Tab = createBottomTabNavigator();

class BottomTab extends React.Component {
    render(){
        return(
            <Tab.Navigator>
                <Tab.Screen name={SCREEN_NAMES.view_events} component={ViewEventsNavigate} />
                <Tab.Screen name={SCREEN_NAMES.friends_list} component={FriendsListNavigate} />
                <Tab.Screen name={SCREEN_NAMES.track_events} component={TrackEvents} />
                <Tab.Screen name={SCREEN_NAMES.create_event} component={CreateEvent} />
                <Tab.Screen name={SCREEN_NAMES.settings} component={Settings} />
            </Tab.Navigator>
        );
    }
}

export default BottomTab;