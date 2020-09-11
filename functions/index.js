const firebase = require("firebase");
const functions = require("firebase-functions");
const admin = require("firebase-admin");
const express = require("express");
const app = express();

const config = require("./.config").firebaseConfig;

admin.initializeApp();
firebase.initializeApp(config);


app.post("/register", (request, response) => {
    const user = {
        email: request.body.email,
        password: request.body.password,
    };

    console.log(user);

    firebase
        .auth()
        .createUserWithEmailAndPassword(user.email, user.password)
        .then((data) => data.user.getIdToken())
        .then((token) => {
            return response.json({ token });
        })
        .catch((err) => response.status(500).json({ error: err.code }));
});


app.post("/login", (request, response) => {
    const user = {
        email: request.body.email,
        password: request.body.password,
    };

    firebase
        .auth()
        .signInWithEmailAndPassword(user.email, user.password)
        .then((data) => data.user.getIdToken())
        .then((token) => response.json({ token }))
        .catch((err) => response.status(500).json({ error: err.code }));
});


app.post("/signout", (request, response) => {
    firebase.auth()
        .signOut()
        // eslint-disable-next-line promise/always-return
        .then(() => {
            console.log("cya");
        })
        .catch((err) => response(500).json({ error: err.code }));
});

exports.api = functions.region("asia-east2").https.onRequest(app);