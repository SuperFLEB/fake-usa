import type {FIPSCode} from "@/typedefs/USState.ts";
import Query from "./Query.ts";
import type {PhoneNumberPrefix, Zip} from "@/typedefs/places";
import toPhoneNumberPrefix from "@/util/toPhoneNumberPrefix.ts";

export type FakePlaceNamesQueryParams = {
	stateFIPSCode: FIPSCode,
	count: number,
	search?: string,
	min?: number,
	max?: number
};
export type FakePlaceNamesQueryResult = {
	featureName: string,
	featureCountAll: number,
	featureCountState: number,
	isSettlement: boolean,
};

export class FakePlaceNamesQuery extends Query<FakePlaceNamesQueryParams, FakePlaceNamesQueryResult> {
	defaultParams = {stateFIPSCode: 1 as FIPSCode, search: "", count: 100, min: 0};

	get sql(): string {
		const {search, min = 0, max = undefined} = this.params;
		return `SELECT feature_name         AS featureName,
                       is_settlement        AS isSettlement,
                       COUNT(*)             AS featureCountAll,
                       COUNT(DISTINCT fips) AS featureCountState
                FROM place_names_existing ${search ? "WHERE feature_name LIKE $search" : ""}
                GROUP BY feature_name
                HAVING SUM(fips = $stateFIPSCode) = 0
                    ${min !== undefined ? "AND COUNT(*) >= $min" : ""} ${max !== undefined ? "AND COUNT(*) <= $max" : ""}
                ORDER BY RANDOM()
                LIMIT $count`;
	}
}

type RegionQueryParams = { fips: FIPSCode };
type RegionQueryResult = { fips: FIPSCode, region: string, subregion: string };

export class RegionQuery extends Query<RegionQueryParams, RegionQueryResult> {
	defaultParams = {fips: 1 as FIPSCode};

	get sql(): string {
		return `SELECT fips, region, subregion
                FROM regions
                WHERE fips = $fips`;
	}
}

export type CallsignQueryParams = { fips: FIPSCode, count: number };
export type CallsignQueryResult = { callsign: string };

export class CallsignQuery extends Query<CallsignQueryParams, CallsignQueryResult> {
	defaultParams = {fips: 1 as FIPSCode, count: 1};

	get sql(): string {
		return `
            WITH kp AS (SELECT k1000 FROM callsigns_k_proportion WHERE fips = $fips LIMIT 1),
                 k AS (SELECT *, (ABS(RANDOM()) / 9223372036854775.8070 < kp.k1000) as chosen
                       FROM main.callsigns_fake
                                CROSS JOIN kp
                       WHERE is_k = TRUE
                         AND kp.k1000 > 0
                       ORDER BY RANDOM()
                       LIMIT $count),
                 notk AS (SELECT *, (ABS(RANDOM()) / 9223372036854775.8070 > kp.k1000) as chosen
                          FROM main.callsigns_fake
                                   CROSS JOIN kp
                          WHERE is_k = FALSE
                            AND kp.k1000 < 1000
                          ORDER BY RANDOM()
                          LIMIT $count)
            SELECT *
            FROM k
            UNION ALL
            SELECT *
            FROM notk
            ORDER BY chosen DESC
            LIMIT $count;
		`;
	}
}

export type TeamQueryParams = { count: number };
export type TeamQueryResult = { name: string };

export class TeamQuery extends Query<TeamQueryParams, TeamQueryResult> {
	defaultParams = {count: 1};

	get sql(): string {
		return `SELECT name
                FROM main.team_names
                ORDER BY RANDOM()
                LIMIT $count`;
	}
}

export type PhoneQueryParams = { npa?: number, fips: FIPSCode, count: number };
export type PhoneQueryResult = PhoneNumberPrefix;

export class PhoneQuery extends Query<PhoneQueryParams, PhoneQueryResult> {
	defaultParams: PhoneQueryParams = {fips: 1, count: 1};
	get sql(): string {
		return `
			WITH RECURSIVE eligible AS MATERIALIZED (
				SELECT
					npa,
					start / 1000  AS first_nxxx,  -- Block start in thousands
					length / 1000 AS block_count, -- Block length in thousands
					SUM(length / 1000) OVER (ORDER BY npa, start) AS cumulative_end  -- Running total of length of this and all prior matched blocks.
				FROM npanxx_fake
				WHERE fips = $fips AND ($npa IS NULL OR npa = $npa)
			),
			bounds AS (SELECT MAX(cumulative_end) AS total FROM eligible),
			draws AS MATERIALIZED (
				SELECT 1 as i, ABS(RANDOM()) % total as block_index FROM bounds WHERE total > 0
				UNION ALL
				SELECT i + 1 AS i, ABS(RANDOM()) % total as block_index FROM draws
				CROSS JOIN bounds
				WHERE i < $count
			)
			SELECT
				(e.npa * 10000 + e.first_nxxx + d.block_index - (e.cumulative_end - e.block_count)) AS npanxxx
			FROM draws AS d
			JOIN eligible AS e
			  ON d.block_index >= e.cumulative_end - e.block_count
			 AND d.block_index < e.cumulative_end
			ORDER BY npanxxx;
		`;
	}

	postprocess(rows: { npanxxx: number }[]): PhoneQueryResult[] {
		return rows.map(row => toPhoneNumberPrefix(row.npanxxx));
	}
}

export type ZipQueryParams = { fips: FIPSCode, level: 0 | 1 | 2 | 3, count: number };
export type ZipQueryResult = Zip;

export class ZipQuery extends Query<ZipQueryParams, ZipQueryResult> {
	defaultParams: ZipQueryParams = {fips: 1 as FIPSCode, level: 0, count: 1};

	get sql(): string {
		return `SELECT *
                FROM zip_fake
                WHERE fips = $fips
                  AND level >= $level
                ORDER BY RANDOM()
                LIMIT $count;`;
	}

	postprocess(rows: { zip: number, level: 0 | 1 | 2 | 3 }[]): ZipQueryResult[] {
		console.log('pp', rows);
		return rows.map((row) => ({number: row.zip, level: row.level}));
	}
}