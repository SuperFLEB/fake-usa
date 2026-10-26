export default function shuffleArrayInPlace<T extends unknown = unknown>(arr: T[]): T[] {
	for (let i = arr.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[arr[i], arr[j]] = [arr[j], arr[i]] as [T, T];
	}
	return arr;
}