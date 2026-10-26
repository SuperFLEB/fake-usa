<script setup lang="ts">
import sqlite3InitModule, {type Database} from "@sqlite.org/sqlite-wasm";
import {onMounted, onUnmounted, provide, ref} from "vue";
import k from "./keys.ts";

type Props = { filePath: string };
const props = defineProps<Props>();
const dbRef = ref<Database | null>(null);

onMounted(() => {
	console.log("Mounted, opening DB ", props.filePath);
	sqlite3InitModule().then(sqlite3 => {
		fetch(props.filePath)
			.then(response => response.arrayBuffer())
			.then(ab => {
				const p = sqlite3.wasm.allocFromTypedArray(ab);
				const db = new sqlite3.oo1.DB();
        if (db.pointer === undefined) throw new Error("Database could not be opened");
				const rc = sqlite3.capi.sqlite3_deserialize(
					db.pointer, "main", p, ab.byteLength, ab.byteLength,
					sqlite3.capi.SQLITE_DESERIALIZE_FREEONCLOSE
					// Optionally:
					// | sqlite3.capi.SQLITE_DESERIALIZE_RESIZEABLE
				);
				db.checkRc(rc);
				return db;
			})
			.then(db => {
				dbRef.value = db;
			});
	});
});

onUnmounted(() => {
	console.log("Unmounted, closing DB ", props.filePath);
	if (!dbRef.value) return;
	dbRef.value.close();
	dbRef.value = null;
});

provide(k.DB_REF, dbRef);
</script>

<template>
	<slot v-if="dbRef"/>
</template>