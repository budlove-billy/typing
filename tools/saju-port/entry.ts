// 플레이말로우용 사주 엔진 묶음 — D:\claude\saju 의 계산·규칙·해석 DB·운세 모듈을 브라우저 한 파일로.
// AI·서버·DB 없이 동작(해석 DB 템플릿 풀이). 빌드: node tools/saju-port/build.mjs
import { analyzeSaju } from "@/features/saju/calculator";
import { RuleEngine } from "@/features/saju/rules";
import { composeReading } from "@/features/saju/interpreter";
import { favorableProfile, dailyFortune, fortuneRange, lifeCurve, monthlyCurve, currentSajuYear, compatibility } from "@/features/saju/fortune";
import { DEFAULT_RULES as RULES } from "@/data/rules";
import { DEFAULT_INTERPRETATIONS as INTERPRETATIONS } from "@/data/interpretations";
export { analyzeSaju, favorableProfile, dailyFortune, fortuneRange, lifeCurve, monthlyCurve, currentSajuYear, compatibility };
export function fullReport(input: any, calc: any, referenceYear: number) {
  const a = analyzeSaju(input, { calculation: calc, referenceYear });
  const { tags } = RuleEngine.evaluate(a, RULES as any, referenceYear);
  const reading = composeReading({ analysis: a, tags, interpretations: INTERPRETATIONS as any, referenceYear } as any);
  return { analysis: a, tags, reading };
}
// 화면 표시용 이름·설명 데이터
export { GLOSSARY } from "@/data/glossary";
export { GYEOKGUK_TEXT, BASIS_TEXT } from "@/data/gyeokguk";
export { TEN_GODS, TEN_GOD_GROUPS, TEN_GOD_RELATIONSHIP } from "@/data/ten-gods";
export { FIVE_ELEMENTS, ELEMENT_ORDER } from "@/data/elements";
export { HEAVENLY_STEMS } from "@/data/stems";
export { EARTHLY_BRANCHES } from "@/data/branches";
export { BIRTH_LOCATIONS } from "@/data/locations";
export { ELEMENT_LUCK, scoreLevel } from "@/data/fortune-texts";
export { STRENGTH_KOREAN, RELATIONSHIP_KOREAN, POSITION_KOREAN } from "@/features/saju/labels";
export { TWELVE_STAGE_KOREAN } from "@/features/saju/calculator/twelve-stages";
export { CATEGORY_KOREAN, compatibilityReport } from "@/features/saju/fortune";
