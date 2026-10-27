export default function arrayPickRandom<T extends any>(array: T[]): T {
	return array[Math.floor(Math.random() * array.length)]!;
}
