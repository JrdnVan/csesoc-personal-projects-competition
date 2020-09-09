import React from 'react';
import { SafeAreaView, View, Text, FlatList, ScrollView } from 'react-native';
import { ListItem } from 'react-native-elements';
import EventCard from '../../components/event_card';

class ViewEvents extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        const DATA = [
            {
                thing: "1"
            },
            {
                thing: "1"
            },
            {
                thing: "1"
            },
            {
                thing: "1"
            },
            {
                thing: "1"
            },
            {
                thing: "1"
            },
            {
                thing: "1"
            },
            {
                thing: "1"
            },
        ];

        const renderItem = ({thing}) => (
            <EventCard navigation={this.props.navigation}/>
        );

        return(
            <SafeAreaView style={{flex: 1}}>
                <FlatList
                    data={DATA}
                    renderItem={renderItem}
                    keyExtractor={item => item.id}
                >
                </FlatList>
            </SafeAreaView>
        );

    }
}
export default ViewEvents;