import { createAppContainer } from 'react-navigation';
import { createStackNavigator } from 'react-navigation-stack';

import Signup from '../../screens/signup'; 
import Login from '../../screens/login';
import BottomTab from '../main_bottom_tab';

import SCREEN_NAMES from './screen_names';

const StackNavigator = createStackNavigator({
    [SCREEN_NAMES.home]: {
        screen: BottomTab
    },
    [SCREEN_NAMES.signup]: {
        screen: Signup
    },
    [SCREEN_NAMES.login]: {
        screen: Login
    },
});

export default createAppContainer(StackNavigator);