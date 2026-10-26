<script setup lang="ts">
import ConfigProvider from "./providers/ConfigProvider/ConfigProvider.vue";
import DBProvider from "@/providers/DBProvider/DBProvider.vue";
import BucketProvider from "@/providers/BucketProvider/BucketProvider.vue";
import "splitpanes/dist/splitpanes.css";
import MainScreen from "@/components/MainScreen.vue";
</script>

<template>
	<DBProvider file-path="./fakeusa.sqlite">
		<ConfigProvider>
			<BucketProvider>
				<MainScreen />
			</BucketProvider>
		</ConfigProvider>
	</DBProvider>
</template>
