import {customRef, type Ref, ref} from "vue";
type DebouncedRef<T> = Ref<T, T> & { raw: Ref<T, T> }
export default function debouncedRef<T>(value: T, delay: number) {
	let timeout: ReturnType<typeof setTimeout>;
	const raw = ref(value) as Ref<T>;
	const cRef = customRef<T>((track, trigger) => ({
			get(): T {
				track();
				return value;
			},
			set(nextValue: T) {
				clearTimeout(timeout);
				raw.value = nextValue;
				timeout = setTimeout(() => {
					value = nextValue;
					trigger();
				}, delay);
			}
		})
	) as DebouncedRef<T>;
	cRef.raw = raw;
	return cRef;
}
