(this.webpackJsonpCourseProject=this.webpackJsonpCourseProject||[]).push([[0],{30:function(t,e,a){},31:function(t,e,a){},32:function(t,e,a){},38:function(t,e,a){"use strict";a.r(e);var s=a(2),n=a(0),i=a.n(n),r=a(20),l=a.n(r),c=(a(30),a(10)),u=a(11),o=a(7),d=a(15),h=a(14),p=(a(31),a(23)),j=a(21),m=function(t){Object(d.a)(a,t);var e=Object(h.a)(a);function a(t){var s;return Object(c.a)(this,a),(s=e.call(this,t)).state={url:"",loading:!1},s.handleChange=s.handleChange.bind(Object(o.a)(s)),s.handleSubmit=s.handleSubmit.bind(Object(o.a)(s)),s.sendRequest=s.sendRequest.bind(Object(o.a)(s)),s}return Object(u.a)(a,[{key:"handleChange",value:function(t){this.setState({url:t.target.value});var e=String(t.target.value).replace(/\/$/,"");this.validateUrl(e)?document.getElementById("input").setCustomValidity("Invalid URL: Make sure you are providing a valid university URL (starts with http(s):// and ends with .edu)."):document.getElementById("input").setCustomValidity("")}},{key:"handleSubmit",value:function(t){if(t.preventDefault(),!this.state.loading){var e=String(this.state.url).replace(/\/$/,"");this.validateUrl(e)?console.log("Invalid URL."):(this.setState({loading:!0}),this.sendRequest())}}},{key:"validateUrl",value:function(t){return!t.endsWith(".edu")||!/^[a-zA-Z:\/\.]+$/.test(t)||!t.startsWith("http://www.")&&!t.startsWith("https://www.")}},{key:"sendRequest",value:function(){var t=this,e={method:"POST",mode:"cors",headers:{"Content-Type":"application/json"},body:JSON.stringify({url:this.state.url})};fetch("https://facultyscraper-heroku.herokuapp.com/",e).then((function(t){if(t.ok)return t.json();throw new Error("Bad response!")})).then((function(e){e.result?(t.setState({loading:!1,url:""}),0==e.urls.length&&document.getElementById("input").setCustomValidity("Failed to get results! Check URL and make sure it is correct. Maybe try with/without the www."),t.props.history.push({pathname:"/results",data:e.urls})):setTimeout(t.sendRequest,1e4)})).catch((function(e){t.setState({loading:!1}),document.getElementById("input").setCustomValidity("Invalid URL! Try another variation of this URL and make sure it is accessible!")}))}},{key:"render",value:function(){return"Faculty Scraper"!=document.title&&(document.title="Faculty Scraper"),[Object(s.jsx)("h1",{className:"title",children:"Faculty Scraper"}),Object(s.jsx)("form",{onSubmit:this.handleSubmit,className:"wrap",children:Object(s.jsxs)("label",{className:"scrape",children:[Object(s.jsx)("input",{autoFocus:!0,type:"text",id:"input",value:this.state.url,onChange:this.handleChange,placeholder:"Input a university URL (e.g. https://www.illinois.edu)",className:"scrapeBar"}),Object(s.jsx)("button",{type:"submit",className:"scrapeButton",children:this.state.loading?Object(s.jsx)(j.a,{}):Object(s.jsx)(p.a,{})})]})})]}}]),a}(i.a.Component),b=(a(32),function(t){Object(d.a)(a,t);var e=Object(h.a)(a);function a(){return Object(c.a)(this,a),e.apply(this,arguments)}return Object(u.a)(a,[{key:"render",value:function(){var t=this.props.location.data;return"Results"!=document.title&&(document.title="Results"),null==t?Object(s.jsx)("h1",{className:"error",children:"Error, no results present!"}):[Object(s.jsx)("h1",{className:"listTitle",children:"Faculty Scraper"}),Object(s.jsx)("hr",{className:"listBar"}),Object(s.jsx)("div",{className:"list",children:t.map((function(t){return Object(s.jsx)("li",{className:"listItem",children:Object(s.jsx)("a",{href:t,target:"_blank",className:"url",children:t})})}))})]}}]),a}(i.a.Component)),y=a(24),v=a(3);l.a.render(Object(s.jsx)(y.a,{children:Object(s.jsxs)("div",{children:[Object(s.jsx)(v.a,{exact:!0,path:"/",component:m}),Object(s.jsx)(v.a,{path:"/results",component:b})]})}),document.getElementById("root"))}},[[38,1,2]]]);
//# sourceMappingURL=main.1996c05d.chunk.js.map