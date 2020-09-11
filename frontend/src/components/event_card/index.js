import React from 'react';
import { View, Text } from 'react-native';
import { Card, Avatar, Button, Divider } from 'react-native-elements';
import Icon from 'react-native-vector-icons/FontAwesome';
import { NavigationActions } from 'react-navigation';
import { StackActions } from 'react-navigation';

import ProfileStackNavigator from '../../screens/view_profile';
import styles from './styles';

class EventCard extends React.Component {
    constructor(props){
        super(props);
        const { navigate } = props.navigation;
        this.navigate = navigate;
    }

    render(){
        return(
            <View
                style={styles.card}
            >
                <View
                    style={styles.flex_row}
                >
                    <Avatar 
                        size="medium"
                        title="JV"
                        rounded
                        activeOpacity={0.7}
                        overlayContainerStyle={{backgroundColor: 'gray'}}
                        onPress={() => {
                            this.props.navigation.navigate('profile', {
                                name: 'test data',
                                last_active: 'test data',
                                avatar_url: ''
                            });
                        }}
                    />
                    <Divider
                        style={{width: 20, backgroundColor: 'opaque'}}
                    />
                    <View>
                        <Text>
                            Location
                        </Text>
                        <Text>
                            Time
                        </Text>
                    </View>
                </View>
                <Text>
                    Description
                </Text>
                <View
                    style={[styles.flex_row, {justifyContent: 'flex-end'}]}
                >
                    <Button
                        style={styles.not_going_button}
                        icon={
                            <Icon
                                name="times"
                                size={25}
                                color="red"
                            />
                        }
                        type="clear"
                    />
                    <Button
                        style={styles.going_button}
                        icon={
                            <Icon
                                name="check"
                                size={25}
                                color="green"
                            />
                        }
                        type="clear"
                    />
                </View>
            </View>
        );

    }
}
export default EventCard;