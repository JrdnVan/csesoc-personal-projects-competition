import React from 'react';
import { View, Text } from 'react-native';
import { Card, Avatar, Button, Divider } from 'react-native-elements';

class ViewProfile extends React.PureComponent {
    constructor(props){
        super(props);
        this.name = props.route.params.name != null ? props.route.params.name : 'Missing name';
        this.last_active = props.route.params.last_active != null ? props.route.params.last_active : "Never";
        this.avatar_url = props.route.params.avatar_url != null ? props.route.params.avatar_url : "";
    }

    render(){
        return(
            <View
                style={{
                    flex: 1,
                    resizeMode: 'cover',
                    backgroundColor: 'white',
                    justifyContent: 'space-between'
                }}
            >
                <View
                    style={{
                        flexDirection: "row"
                    }}
                >
                <Avatar source={{uri: this.avatar_url}} rounded/>
                    <Divider
                        style={{width: 20, backgroundColor: 'opaque'}}
                    />
                    <View
                        style={{
                            flexDirection: "column"
                        }}
                    >
                        <Text>
                            {this.name}
                        </Text>
                        <Text>
                            {this.last_active}
                        </Text>
                    </View>
                    <Text>
                        mute
                    </Text>
                </View>
                <Button
                    title='ADD/ACCEPT/REJECT/REMOVE'
                />
            </View>
        );

    }
}
export default ViewProfile;