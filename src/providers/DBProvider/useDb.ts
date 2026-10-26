import {inject, type Ref, toRaw} from "vue";
import {ComposableOutOfContextError} from "@/errors.ts";
import k from "./keys.ts"
import type {Database} from "@sqlite.org/sqlite-wasm";

export default function useDb(): () => Database {
	const dbRef = inject<Ref<Database>>(k.DB_REF);
	if (!dbRef) throw new ComposableOutOfContextError("useDb must be run inside a DBProvider");
	return () => {
		const dbRefValue = dbRef.value;
		if (!dbRefValue) throw new Error("Database reference could not be resolved");
		return toRaw(dbRefValue);
	}
}
