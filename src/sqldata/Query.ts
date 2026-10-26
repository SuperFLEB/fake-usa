import type {BindableValue, BindingSpec, Database, PreparedStatement} from "@sqlite.org/sqlite-wasm";

function execAndGetAll<T extends Record<string, any> = Record<string, any>>(stmt: PreparedStatement): T[] {
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

function toBinding(obj: Record<string, unknown>, stmt: PreparedStatement): BindingSpec {
	const binding: BindingSpec = {};
	for (const k of Object.keys(obj)) {
		if (stmt.getParamIndex(`$${k}`)) binding[`$${k}`] = obj[k] as BindableValue;
	}
	return binding;
}

export default abstract class Query<TParam extends Record<string, unknown> = Record<string, unknown>, TSingleResult extends Record<string, unknown> = Record<string, unknown>> {
	db: Database;

	protected _params?: Partial<TParam>;
	protected abstract defaultParams: TParam;

	protected sql_string?: string;
	protected get sql(): string {
		return this.sql_string ?? '';
	}

	get params(): TParam {
		const params = {...this.defaultParams, ...this._params as Partial<TParam>} as TParam;
		this._params = params;
		return params;
	}

	set params(params: Partial<TParam>) {
		this._params = {...this.params, ...params};
	}

	prepare(): PreparedStatement {
		const prepared = this.db.prepare(this.sql);
		prepared.bind(toBinding(this.params, prepared));
		return prepared;
	}

	execute(): TSingleResult[] {
		const prepared = this.prepare();
		try {
			return this.postprocess(execAndGetAll<TSingleResult>(prepared));
		} finally {
			prepared.finalize();
		}
	}

	postprocess(rows: Record<string, unknown>[]): TSingleResult[] {
		return rows as TSingleResult[];
	}

	constructor(db: Database, params?: Partial<TParam>) {
		this.db = db;
		if (params) this._params = params;
	}
}
