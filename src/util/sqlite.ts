import {PreparedStatement} from "@sqlite.org/sqlite-wasm";

export function execAndGetAll<T extends Record<string, any> = Record<string, any>>(stmt: PreparedStatement): T[] {
	const columns = stmt.getColumnNames() as (keyof T)[];
	const output = [];
	while (stmt.step()) {
		const row = {} as T;
		for (let colIdx = 0; colIdx < columns.length; colIdx++) {
			row[columns[colIdx] as keyof T] = stmt.get(colIdx) as T[typeof columns[number]];
		}
		output.push(row);
	}
	return output;
}