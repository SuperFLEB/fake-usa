<script setup lang="ts">
import useConfigProvider from "../providers/ConfigProvider/useConfigProvider.ts";
import StatePicker from "@/components/StatePicker.vue";
import {computed} from "vue";
import {STATE_NAME_BY_FIPS} from "@/typedefs/USState.ts";
const {stateFIPSCode} = useConfigProvider();
</script>

<template>
	<StatePicker v-model="stateFIPSCode" />
</template>

<style scoped>

</style>