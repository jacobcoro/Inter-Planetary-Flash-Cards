import { ValidationRule, ValidationRuleSchema, RuleParamConfig } from './types';
interface NormalizedRuleSchema extends ValidationRuleSchema {
    params?: RuleParamConfig[];
}
declare type RuleIterateFn = (ruleName: string, schema: NormalizedRuleSchema) => any;
export declare class RuleContainer {
    static extend(name: string, schema: ValidationRuleSchema): void;
    static iterate(fn: RuleIterateFn): void;
    static isLazy(name: string): boolean;
    static isRequireRule(name: string): boolean;
    static isTargetRule(name: string): boolean;
    static getRuleDefinition(ruleName: string): NormalizedRuleSchema;
}
/**
 * Adds a custom validator to the list of validation rules.
 */
export declare function extend(name: string, schema: ValidationRule): void;
export {};
