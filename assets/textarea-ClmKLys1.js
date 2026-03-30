import{c as n,f as c}from"./index-B0HQVBH5.js";import{j as u}from"./react-vendor-DViTTRkQ.js";import{u as x,g}from"./input-R2TtqV7M.js";/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const h=n("Star",[["polygon",{points:"12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2",key:"8f66p6"}]]);/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const v=n("Trash2",[["path",{d:"M3 6h18",key:"d0wm0j"}],["path",{d:"M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6",key:"4alrt4"}],["path",{d:"M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2",key:"v07s0e"}],["line",{x1:"10",x2:"10",y1:"11",y2:"17",key:"1uufr5"}],["line",{x1:"14",x2:"14",y1:"11",y2:"17",key:"xtxkd"}]]);function b({className:i,onKeyDown:e,onCompositionStart:s,onCompositionEnd:a,...r}){const t=x(),{onCompositionStart:d,onCompositionEnd:p,onKeyDown:m}=g({onKeyDown:o=>{const l=o.nativeEvent.isComposing||t.justEndedComposing();o.key==="Enter"&&!o.shiftKey&&l||e?.(o)},onCompositionStart:o=>{t.setComposing(!0),s?.(o)},onCompositionEnd:o=>{t.markCompositionEnd(),setTimeout(()=>{t.setComposing(!1)},100),a?.(o)}});return u.jsx("textarea",{"data-slot":"textarea",className:c("border-input placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive dark:bg-input/30 flex field-sizing-content min-h-16 w-full rounded-md border bg-transparent px-3 py-2 text-base shadow-xs transition-[color,box-shadow] outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",i),onCompositionStart:d,onCompositionEnd:p,onKeyDown:m,...r})}export{h as S,v as T,b as a};
