import { createApp } from "vue";
import { createPinia } from "pinia";
import { createAuth0 } from '@auth0/auth0-vue';

import "./assets/main.css";

import App from "./App.vue";
import VueDragscroll from "vue-dragscroll";

const app = createApp(App);

app.use(VueDragscroll);
app.use(createPinia());
app.use(
    createAuth0({
        domain: import.meta.env.VITE_AUTH0_DOMAIN,
        client_id: import.meta.env.VITE_AUTH0_CLIENT_ID,
        redirect_uri: window.location.origin
    })
)

app.mount("#app");
