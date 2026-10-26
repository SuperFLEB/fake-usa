import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import {STATE_BY_FIPS} from "@/typedefs/USState.ts";
import shuffleArrayInPlace from "@/util/shuffleArrayInPlace.ts";
import dynamicBackground from "@/dynamicBackground.ts";

createApp(App).mount('#app')
const dynamicBackgroundImageURL = await dynamicBackground();
document.documentElement.style.setProperty('--dynamic-background-image', `url(${dynamicBackgroundImageURL})`);
