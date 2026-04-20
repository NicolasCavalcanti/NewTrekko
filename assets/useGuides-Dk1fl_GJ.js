import{c as o,t as s,f as u}from"./index-DLIen7SN.js";import{r as n}from"./react-vendor-DViTTRkQ.js";/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const y=o("Globe",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20",key:"13o1zl"}],["path",{d:"M2 12h20",key:"9i4pu4"}]]);/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const g=o("Phone",[["path",{d:"M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z",key:"foiqr5"}]]),a=!1,d="/";function r(){return u({queryKey:["static-guides"],queryFn:async()=>{const e=`${d}data/guides.json`,t=await fetch(e);if(!t.ok)throw new Error(`Failed to load ${e}: ${t.status}`);return t.json()},enabled:a,staleTime:1/0})}function f(e){const t=r(),i=s.guides.list.useQuery(e,{enabled:!a,staleTime:6e4});return n.useMemo(()=>{},[t.data,e.search,e.cadasturCode,e.uf,e.city,e.page,e.limit]),{data:i.data,isLoading:i.isLoading}}function h(e){r();const t=s.guides.getById.useQuery({cadasturNumber:e},{enabled:!a});return{data:t.data,isLoading:t.isLoading,error:t.error}}function L(e){const t=r(),i=s.guides.getCities.useQuery({uf:e&&e!=="all"?e:void 0},{enabled:!a});return n.useMemo(()=>{},[t.data,e]),{data:i.data,isLoading:i.isLoading}}export{y as G,g as P,f as a,h as b,L as u};
