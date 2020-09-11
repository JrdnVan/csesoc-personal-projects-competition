import React from 'react';
import { ListItem, Avatar, ThemeProvider } from 'react-native-elements'
import { SafeAreaView, View, Text, FlatList, ScrollView } from 'react-native';

class FriendsList extends React.Component {
    constructor(props){
        super(props);
    }
    keyExtractor = (item, index) => index.toString()

    renderItem = ({ item }) => (
        <ThemeProvider theme={{  
            colors: {
              platform: {
                "default": {
                  "grey": "#FFF"
                }
              }
            }
          }}>
            <ListItem bottomDivider 
                onPress={() => {
                    this.props.navigation.navigate('profile', {
                        name: item.name,
                        avatar_url: item.avatar_url,
                        last_active: 'never'
                    });
                }}
            >
            <Avatar source={{uri: item.avatar_url}} rounded/>
            <ListItem.Content>
                <ListItem.Title>{item.name}</ListItem.Title>
                <ListItem.Subtitle>{item.subtitle}</ListItem.Subtitle>
            </ListItem.Content>
            <ListItem.Chevron />
            </ListItem>

        </ThemeProvider>
      )

    render(){
        const list = [
            {
              name: 'Amy Farha',
              avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg',
              subtitle: 'Vice President'
            },
            {
              name: 'Chris Jackson',
              avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/adhamdannaway/128.jpg',
              subtitle: 'Vice Chairman'
            },
            {
                name: 'Amy Farha',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg',
                subtitle: 'Vice President'
              },
              {
                name: 'Chris Jackson',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/adhamdannaway/128.jpg',
                subtitle: 'Vice Chairman'
              },
              {
                name: 'Amy Farha',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg',
                subtitle: 'Vice President'
              },
              {
                name: 'Chris Jackson',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/adhamdannaway/128.jpg',
                subtitle: 'Vice Chairman'
              },            {
                name: 'Amy Farha',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg',
                subtitle: 'Vice President'
              },
              {
                name: 'Chris Jackson',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/adhamdannaway/128.jpg',
                subtitle: 'Vice Chairman'
              },            {
                name: 'Amy Farha',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg',
                subtitle: 'Vice President'
              },
              {
                name: 'Chris Jackson',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/adhamdannaway/128.jpg',
                subtitle: 'Vice Chairman'
              },            {
                name: 'Amy Farha',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg',
                subtitle: 'Vice President'
              },
              {
                name: 'Chris Jackson',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/adhamdannaway/128.jpg',
                subtitle: 'Vice Chairman'
              },            {
                name: 'Amy Farha',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg',
                subtitle: 'Vice President'
              },
              {
                name: 'Chris Jackson',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/adhamdannaway/128.jpg',
                subtitle: 'Vice Chairman'
              },            {
                name: 'Amy Farha',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg',
                subtitle: 'Vice President'
              },
              {
                name: 'Chris Jackson',
                avatar_url: 'https://s3.amazonaws.com/uifaces/faces/twitter/adhamdannaway/128.jpg',
                subtitle: 'Vice Chairman'
              },
        ]
        return(
            <SafeAreaView style={{flex: 1}}>
                <FlatList
                keyExtractor={this.keyExtractor}
                data={list}
                renderItem={this.renderItem}
                />
            </SafeAreaView>
        );

    }
}
export default FriendsList;