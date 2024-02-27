console.log("extens.js loading...")

var app = {};
    app.launchTime=now();
    app.ready=false;
    app.activeMenu="";
    app.fooocusUrl="";     app.fooocusPort=0;     app.fooocusHost="";
    app.pingFoooxus=0;      app.nbPingFoooxus=0;    app.lastPingFoooxusOk=0;    app.foooxusConnection=false;
    app.pingFooocus=0;      app.nbPingFooocus=0;    app.lastPingFooocusOk=0;    app.fooocusConnection=false;
    app.models=[];
    app.loras=[];
    app.device=null;
    app.config=false;
    app.jsons=[];           /* jsons that are prepared to send to API */
    app.calls=[];           /* jsons that are sent to API */
    app.activeCall=-1;        
    app.generating=false;
    app.illustrationsFolder="outputs/illustrations";
    app.illustrations={
        lastCheck:0,
        models:[],
        styles:[],
        loras:[]
    }
    app.ratios=["1024×1024", "704×1408", "768×1280", "768×1344", "896×1152", "1408×704", "1280×768", "1344×768", "1152×896"];


$( document ).ready(function() {
    console.log("extens.js loaded")
    console.log("document Ready")
    startApp();
})

var metadataBase={
    "Prompt":"a cat in the kitchen",
    "Negative Prompt":"",
    "Styles":[],
    "Performance":"Speed",
    "Resolution":"(1024, 1024)",
    "Guidance Scale":4,
    "Sharpness":2,
    "ADM Guidance":"(1.5, 0.8, 0.3)",
    "Base Model":"juggernautXL_v8Rundiffusion.safetensors",
    "Alternative Model":"",
    "Refiner Model":"None",
    "Refiner Switch":0.1,
    "Sampler":"dpmpp_2m_sde_gpu",
    "Scheduler":"karras",
    "Seed":"314159",
    "Lora 1":"None",
    "Weight Lora 1": 0.1,
    "Lora 2":"None",
    "Weight Lora 2": 0.1,
    "Lora 3":"None",
    "Weight Lora 3": 0.1,
    "Lora 4":"None",
    "Weight Lora 4": 0.1,
    "Lora 5":"None",
    "Weight Lora 5": 0.1
}



function activateMenu(menu) {
    app.activeMenu=menu;
    if (menu!="menu-help") {
        $("div#help").hide();
        $("div#app").show();
    } else {
        $("div#help").show();
        $("div#app").hide();
    }
    $("span.menu-nav-link").removeClass("active");
    $("span#"+menu).addClass("active");
}

function displayConnectionFooocus() {
    if (app.fooocusConnection) {  $("span#fooocusConnection").removeClass("IPdisconnected").removeClass("IPwaiting").addClass("IPconnected"); } 
    else { $("span#fooocusConnection").removeClass("IPconnected").removeClass("IPwaiting").addClass("IPdisconnected");   } 
}
function displayConnectionFoooxus() {
    if (app.foooxusConnection) { $("span#foooxusConnection").removeClass("IPdisconnected").removeClass("IPwaiting").addClass("IPconnected"); } 
    else { $("span#foooxusConnection").removeClass("IPconnected").removeClass("IPwaiting").addClass("IPdisconnected"); } 
}

function displayConnections() {displayConnectionFooocus(); displayConnectionFoooxus();}


/* Update the foooxus queue and the foooocus running buttons */
function displayQueue() {
    /* Foooxus */
    if ((app.activeCall==-1)||(app.calls.length-app.activeCall<=0)) {
        $("#foooxusQueue").removeClass("btn-success").addClass("btn-secondary");
        $("#foooxusQueue span").html(""); 
    } else {
        $("#foooxusQueue").removeClass("btn-secondary").addClass("btn-success");
        $("#foooxusQueue span").html(app.calls.length-app.activeCall-1);
    }

    /* Fooocus */
    if (app.generating) {
        $("#fooocusQueue").removeClass("btn-secondary").addClass("btn-success");
        $("#fooocusQueue span").html("1");
        $("#fooocusQueue i").addClass("fa-person-running").removeClass("fa-snowflake");    
    } else {
        $("#fooocusQueue").removeClass("btn-success").addClass("btn-secondary");
        $("#fooocusQueue span").html("");    
        $("#fooocusQueue i").addClass("fa-snowflake").removeClass("fa-person-running");    
    }
}

/* Update the queue and connection status of the app */
function updateHeader() {
    if (app.step==1) {
        $("span#foooxusConnection").html(app.host+":"+app.port);
        $("span#introFoooxusURL").html(app.host+":"+app.port);
    } 
    if (app.step==4) {
        $("span#fooocusConnection").html(app.fooocusHost+":"+app.fooocusPort);
        $("span#introFooocusURL").html(app.fooocusHost+":"+app.fooocusPort);
    } 
    displayQueue();
}


/* Ping Foooxus and Fooocus to check connexions */
function pingAll() {
    pingFoooxus(function() {
        if (app.foooxusConnection==false) {
            /* Connexion restored */
            new jBox('Notice', {
                content: 'FoooXus connexion restored <i class="fa-solid fa-link"></i>',
                color: 'green'
            });    
            app.foooxusConnection=true;
            displayConnections();            
        }
    }, function() {
        if (app.foooxusConnection==true) {
            /* Foooxus Connexion Lost */
            new jBox('Notice', {
                content: 'FoooXus connexion lost <i class="fa-solid fa-link-slash"></i>',
                color: 'red'
            });            
            app.foooxusConnection=false;
            app.fooocusConnection=false;
            displayConnections();
        }
    })

    if (app.foooxusConnection) {
        pingFooocus(function() {
            if (app.fooocusConnection==false) {
                /* Connexion restored */
                new jBox('Notice', {
                    content: 'Fooocus connexion restored <i class="fa-solid fa-link"></i>',
                    color: 'green'
                });    
                app.fooocusConnection=true;
                displayConnections();
            }
        }, function() {
            if (app.fooocusConnection==true) {
                /* Foooxus Connexion Lost */
                new jBox('Notice', {
                    content: 'Fooocus connexion lost <i class="fa-solid fa-link-slash"></i>',
                    color: 'red'
                });            
                app.fooocusConnection=false;
                displayConnections();
            }
        })
    }
}


function pingFooocusLost() {
    $("#label-step").html("Connection to Fooocus App not found <i class='fas fa-exclamation-triangle'></i><br>Launch Fooocus and refresh this page ");
    $("#containerStep").css("background-color", "#f00").css("color", "#fff");

    app.fooocusConnection=false;
}

/* Launch app when document is ready */
async function startApp(){
    console.log("startApp() called")

    $('.queue-tooltip').jBox('Tooltip', {
        theme: 'TooltipDark'
    });

    app.host=window.location.hostname;
    app.port=window.location.port;

    /* Step 1 */ 
    updateStep(1);
    await timer(500);
    
    pingFoooxus(async function() {
        /* Step 2 */
        updateStep(2);
        await timer(50);
        getDeviceInfo(async function () {
            /* Step 3 */
            updateStep(3);
            await timer(750);
            showDeviceInfo();
            pingFooocus(async function() {
                /* Step 4 */
                updateStep(4);
                await timer(10);
                getModels(async function() {
                    /* Step 5 */
                    updateStep(5);
                    getStyles();
                    getLoras();
                    console.log("App READY");
                    getIllustrations();
                    if (app.config.messageConfig!="") {
                        $("p#messageApp").html(`<div class="alert alert-warning" role="alert">
                        ${app.config.messageConfig}
                      </div>`)
                    }
                    $("div#app").show();
                    setTimeout(function() {
                        app.ready=true;
                        makeAppHelp();
                    }, 100);
                    setTimeout(function() {
                        $("div#loading").hide();
                    }, 1000);
                });    
            }, function() {
                pingFooocusLost();
            });
        });         
    });
    
}

/* Button to select/deselect all checkbox in front of models */
function checkAllModels(val) {
    for (var i=0; i<app.models.length; i++) {
        $("input#model-"+i).prop("checked", val);
    }
    return false;
}


/* Prepare the generation of preset lora illustrations */
function generatePresetLoraIllustration(numPreset, name, loras=[]) {
    console.log("generatePresetLoralIllustration("+numPreset+")")
    let jsons=[];
    if (loras=="all") {
        loras=[];
        for (let i=0; i<app.loras.length; i++) {
            loras.push(i);
        }
    }
    for (let i=0; i<loras.length; i++) {
        let lora=app.loras[loras[i]];
        let json=JSON.parse(JSON.stringify(Object.assign(metadataBase, app.config["lora-illustrations"][numPreset].metadata)));
        jsons[i]=json;
        jsons[i]["action"]={
            "resize": app.config.illustrationResizeSizes,
            "compress": app.config.illustrationResizeCompress,
            "copy": app.illustrationsFolder+"/loras/"+secureFile(lora.replace(".safetensors", ""))+"_"+secureFile(name)+".jpg"
        }
        jsons[i]["Lora 1"]=lora;
        jsons[i]["desc"]=`Lora [${lora}] Illustration [${name}] : Prompt="${json.Prompt}" `;
    }
    app.jsons=jsons;
    new jBox('Notice', {
        content: "Generation of "+jsons.length+" illustrations for <strong>"+secure(name)+" : "+secure(app.config["lora-illustrations"][numPreset].description)+"</strong> illustration lora preset",
        color: 'green'
    });
    launchGeneration(function(data) {
        let src=data.metadata.action.copy;
        let id=src.replace(app.illustrationsFolder+"/loras/", "").replace(".jpg", "" );
        console.log(src, id)
        $("div#"+id).html(`<img src="${src}" loading="lazy" class="responsive thumbnail">`);
    });
}

function makeAppLoras() {
    if (!app.ready) return;
    activateMenu("menu-loras");
    $("div#app").html("");

    if (app.loras.length==0) {
        $("div#app").html(`
        <div class="alert alert-warning" role="alert">
            <p>No LoRA found in the folder <b>${secure(app.config["loras-directory"])}</b></p>
            <p>Check the <b>config.json</b> file and fill in the <b>fooocus-directory</b> value.</p>
        </div>`)
        return;
    }

    let form=$("<form>").attr("id", "form-app");
    let loras="";
    let illustrations=app.illustrations.loras;
    let generates=[];
    for (let i=0; i<app.config["lora-illustrations"].length; i++) {
        generates[i]=[];
    }

    for (let i=0; i<app.loras.length; i++) {
        let pics="";
        for (let j=0; j<app.config["lora-illustrations"].length; j++) {
            let id=secureFile(app.loras[i].replace(".safetensors", ""))+"_"+(app.config["lora-illustrations"][j].name);
            let src=id+".jpg";
            if (illustrations.includes(src)) {
                pics+=`<div class="col p-2px imgViewer" id="${id}"><img src="${app.illustrationsFolder}/loras/${src}" loading="lazy" class="responsive thumbnail img-enlargeable" title="LORA: ${secure(app.loras[i].replace(".safetensors", ""))} / PRESET: ${secure(app.config["lora-illustrations"][j].name)}"></div>`;
            } else {
                /* This lora #i doesn't have this illustration #k yet */
                pics+=`<div class="col p-2px imgViewer" id="${id}"></div>`;
                generates[j].push(i);
            }
        }
        if (pics=="") { 
            pics="No illustration generated yet";
        } else {
            pics="<div id='lora"+i+"' class='row'>"+pics+"</div>";
        }
        loras+=`
            <div class="lora-item" id="lora-${i}">
                <div class="titre-lora fs-5 font-weight-bold">${app.loras[i].replace(".safetensors", "")}</div>
                <div class="row row-cols-auto mb-1">${pics}</div>
            </div>
        `
    }
    let presets="";
    for (let i=0; i<app.config["lora-illustrations"].length; i++) { 
        let preset=app.config["lora-illustrations"][i];
        let btn=`
         <button type="button" class="btn btn-sm btn-primary display-inline m-1 p-0 px-1 fs-12px" onclick="generatePresetLoraIllustration(${i}, '${secure(preset.name)}', [${generates[i].toString()}])">
        Generate illustrations for ${generates[i].length} loras that don't have it yet
        </button>
        <br>`
        if (generates[i].length==0) {btn="";}
        let title=secure("Grid view of "+app.loras.length+" loras for the ["+preset.name+" - Prompt= "+preset.metadata.Prompt+"]");
        /* Check if model exists in models list or replace it */
        let htmlModel="";
        let checkModel=checkModelExists(preset.metadata["Base Model"]);
        if (checkModel===true) {
            htmlModel=""+secure(preset.metadata["Base Model"].replace(".safetensors",""))
        } else {
            app.config["lora-illustrations"][i].metadata["Alternative Model"]=checkModel
            htmlModel=`<span class="badge bg-warning">${secure(preset.metadata["Base Model"].replace(".safetensors",""))} not found</span><br>
            ${secure(checkModel.replace(".safetensors",""))}`
        }


        presets+=`            
        <td class="fs-13px" style="width: ${100/app.config["lora-illustrations"].length}%">
            <div class="text-center preset-name">
                ${secure(preset.name)}
                <button type="button" class="btn btn-sm btn-success display-inline m-1 p-0 px-1 fs-12px" onclick="gridViewIllustration('loras', '${secure(preset.name)}', 6, '${title}')">Grid view</button>
            </div>
            <div class="text-prompt">${secure(preset.metadata.Prompt)} </div>
            <div class="preset-param">Seed: ${secure(preset.metadata.Seed)} </div>
            <div class="preset-param">Styles: ${secure(preset.metadata.Styles.join(", "))} </div>
            <div class="preset-param">${htmlModel} </div>
            
            <div class="text-center">
                ${btn}
                <button type="button" class="btn btn-sm btn-danger display-inline m-1 p-0 px-1 fs-12px" onclick="generatePresetLoraIllustration(${i}, '${secure(preset.name)}', 'all')">Regenerate all illustrations</button>
            </div>
        </td>
        `
    }

    form.html(`
    <div class="container p-0 m-0">
        <h2>Your Fooocus installation gets ${app.loras.length} loras</h2>
        <div class="">Here is the list of illustration presets that can be generated with your Fooocus installation for each lora.</div>
        <div class="text-help">You can edit/modify/add the list of presets in the <code>config.json</code> file in the FoooXus app folder. <button type="button" class="btn btn-sm btn-primary  py-0 m-0" onclick="viewHelpConfigPreset()">View help about Presets</button></div>
        <table class="table">
        <tbody>
        <tr>
            ${presets}
        </tr>
        </tbody>
        </table>
        <div class="row mt-2">
            <div class="container p-0">
                <div class="mb-1 row">                    
                    <div class="col"><b>Loras in your Fooocus folder</b></div>
                    <div  class="col"><input type="search" placeholder="Filter models by name" class="form-control" id="filter-loras" name="filter-loras"  onkeyup="filterLoras(this.value)"  onsearch="filterLoras(this.value)"> </div>
                    <div  class="col"s><span id="filter-nb-models"></span></div>
                </div>
                <div class="mb-1">
                    ${loras}
                </div>
            </div>
        </div>
    </div>
    `);

    $("div#app").append(form);
    setTimeout(function() {madeImgEnlargeable()}, 100);

}



/* Prepare the generation of preset model illustrations */
function generatePresetModelIllustration(numPreset, name, models=[]) {
    console.log("generatePresetModelIllustration("+numPreset+")")
    let jsons=[];
    if (models=="all") {
        models=[];
        for (let i=0; i<app.models.length; i++) {
            models.push(i);
        }
    }
    for (let i=0; i<models.length; i++) {
        let model=app.models[models[i]];
        let json=JSON.parse(JSON.stringify(Object.assign(metadataBase, app.config["model-illustrations"][numPreset].metadata)));
        jsons[i]=json;
        jsons[i]["action"]={
            "resize": app.config.illustrationResizeSizes,
            "compress": app.config.illustrationResizeCompress,
            "copy": app.illustrationsFolder+"/models/"+secureFile(model.replace(".safetensors", ""))+"_"+secureFile(name)+".jpg"
        }
        jsons[i]["Base Model"]=model;
        jsons[i]["desc"]=`Model [${model}] Illustration [${name}] : Prompt="${json.Prompt}" `;
    }
    app.jsons=jsons;
    new jBox('Notice', {
        content: "Generation of "+jsons.length+" illustrations for <strong>"+secure(name)+" : "+secure(app.config["model-illustrations"][numPreset].description)+"</strong> illustration model preset",
        color: 'green'
    });
    launchGeneration(function(data) {
        let src=data.metadata.action.copy;
        let id=src.replace(app.illustrationsFolder+"/models/", "").replace(".jpg", "" );
        console.log(src, id)
        $("div#"+id).html(`<img src="${src}" loading="lazy" class="responsive thumbnail">`);
    });
}

/* Tab of models UI, view and generate all preset model illustrations */
function makeAppModels() {
    if (!app.ready) return;
    activateMenu("menu-models");

    $("div#app").html("");
    let form=$("<form>").attr("id", "form-app");
    let models="";
    let illustrations=app.illustrations.models;
    let generates=[];
    for (let i=0; i<app.config["model-illustrations"].length; i++) {
        generates[i]=[];
    }

    for (let i=0; i<app.models.length; i++) {
        let pics="";
        for (let j=0; j<app.config["model-illustrations"].length; j++) {
            let id=secureFile(app.models[i].replace(".safetensors", ""))+"_"+(app.config["model-illustrations"][j].name);
            let src=id+".jpg";
            if (illustrations.includes(src)) {
                pics+=`<div class="col p-2px imgViewer" id="${id}"><img src="${app.illustrationsFolder}/models/${src}" loading="lazy" class="responsive thumbnail img-enlargeable" title="MODEL: ${secure(app.models[i].replace(".safetensors", ""))} / PRESET: ${secure(app.config["model-illustrations"][j].name)}"></div>`;
            } else {
                /* This model #i doesn't have this illustration #k yet */
                pics+=`<div class="col p-2px imgViewer" id="${id}"></div>`;
                generates[j].push(i);
            }
        }
        if (pics=="") { 
            pics="No illustration generated yet";
        } else {
            pics="<div id='model"+i+"' class='row'>"+pics+"</div>";
        }
        models+=`
            <div class="model-item" id="model-${i}">
                <div class="titre-model fs-5 font-weight-bold">${app.models[i].replace(".safetensors", "")}</div>
                <div class="row row-cols-auto mb-1">${pics}</div>
            </div>
        `
    }
    let presets="";
    for (let i=0; i<app.config["model-illustrations"].length; i++) { 
        let preset=app.config["model-illustrations"][i];
        let btn=`
         <button type="button" class="btn btn-sm btn-primary display-inline m-1 p-0 px-1 fs-12px" onclick="generatePresetModelIllustration(${i}, '${secure(preset.name)}', [${generates[i].toString()}])">
        Generate illustrations for ${generates[i].length} models that don't have it yet
        </button>
        <br>`
        if (generates[i].length==0) {btn="";}
        let title=secure("Grid view of "+app.models.length+" models for the ["+preset.name+" - Prompt= "+preset.metadata.Prompt+"]");
        presets+=`            
        <td class="fs-13px" style="width: ${100/app.config["model-illustrations"].length}%">
            <div class="text-center preset-name">
                ${secure(preset.name)}
                <button type="button" class="btn btn-sm btn-success display-inline m-1 p-0 px-1 fs-12px" onclick="gridViewIllustration('models', '${secure(preset.name)}', 6, '${title}')">Grid view</button>

            </div>
            <div class="text-prompt">${secure(preset.metadata.Prompt)} </div>
            <div class="preset-param">Seed: ${secure(preset.metadata.Seed)} </div>
            <div class="preset-param">Styles: ${secure(preset.metadata.Styles.join(", "))} </div>
            <div class="text-center">
                ${btn}
                <button type="button" class="btn btn-sm btn-danger display-inline m-1 p-0 px-1 fs-12px" onclick="generatePresetModelIllustration(${i}, '${secure(preset.name)}', 'all')">Regenerate all illustrations</button>
            </div>
        </td>
        `
    }

    form.html(`
    <div class="container p-0 m-0">
        <h2>Your Fooocus installation gets ${app.models.length} models</h2>
        <div class="">Here is the list of illustration presets that can be generated with your Fooocus installation for each model.</div>
        <div class="text-help">You can edit/modify/add the list of presets in the <code>config.json</code> file in the FoooXus app folder. <button type="button" class="btn btn-sm btn-primary  py-0 m-0" onclick="viewHelpConfigPreset()">View help about Presets</button></div>
        <table class="table">
        <tbody>
        <tr>
            ${presets}
        </tr>
        </tbody>
        </table>
        <div class="row mt-2">
            <div class="container p-0">
                <div class="mb-1 row">                    
                    <div class="col"><b>Models in your Fooocus folder</b></div>
                    <div  class="col"><input type="search" placeholder="Filter models by name" class="form-control" id="filter-models" name="filter-models"  onkeyup="filterModels(this.value)" onsearch="filterModels(this.value)"> </div>
                    <div  class="col"s><span id="filter-nb-models"></span></div>
                </div>
                <div class="mb-1">
                    ${models}
                </div>
            </div>
        </div>
    </div>
    `);

    $("div#app").append(form);

    setTimeout(function() {madeImgEnlargeable()}, 100);
}

/* Prepare the generation of preset style illustrations */ 
function generatePresetStyleIllustration(numPreset, name, styles=[]) {
    console.log("generatePresetStyleIllustration("+numPreset+")")
    let jsons=[];
    if (styles=="all") {
        styles=[];
        for (let i=0; i<app.styles.length; i++) {
            styles.push(i);
        }
    }
    for (let i=0; i<styles.length; i++) {
        let style=app.styles[styles[i]];
        let json=JSON.parse(JSON.stringify(Object.assign(metadataBase, app.config["style-illustrations"][numPreset].metadata)));
        jsons[i]=json;
        jsons[i]["action"]={
            "resize": app.config.illustrationResizeSizes,
            "compress": app.config.illustrationResizeCompress,
            "copy": app.illustrationsFolder+"/styles/"+secureFile(style)+"_"+secureFile(name)+".jpg"
        }
        jsons[i]["Styles"]=[style];
        jsons[i]["desc"]=`Style [${style}] Illustration [${name}] : Prompt="${json.Prompt}" `;
    }
    app.jsons=jsons;
    new jBox('Notice', {
        content: "Generation of "+jsons.length+" illustrations for <strong>"+secure(name)+" : "+secure(app.config["style-illustrations"][numPreset].description)+"</strong> illustration style preset",
        color: 'green'
    });
    launchGeneration(function(data) {
        let src=data.metadata.action.copy;
        let id=src.replace(app.illustrationsFolder+"/styles/", "").replace(".jpg", "" );
        console.log(src, id)
        $("div#"+id).html(`<img src="${src}" loading="lazy" class="responsive thumbnail">`);
    });
}

/* Tab of styles UI, view and generate all preset style illustrations */
function makeAppStyles() {
    if (!app.ready) return;
    activateMenu("menu-styles");

    $("div#app").html("");
    let form=$("<form>").attr("id", "form-app");

    let styles=""; 
    let illustrations=app.illustrations.styles;
    let generates=[];
    for (let i=0; i<app.config["style-illustrations"].length; i++) {
        generates[i]=[];
    }

    for (let i=0; i<app.styles.length; i++) {
        let pics="";
        for (let j=0; j<app.config["style-illustrations"].length; j++) {
            let id=secureFile(app.styles[i])+"_"+(app.config["style-illustrations"][j].name);
            let src=id+".jpg";
            if (illustrations.includes(src)) {
                pics+=`<div class="col p-2px imgViewer" id="${id}"><img src="${app.illustrationsFolder}/styles/${src}" loading="lazy" class="responsive thumbnail img-enlargeable" title="STYLE: ${secure(app.styles[i])} / PRESET: ${secure(app.config["style-illustrations"][j].name)}"></div>`;
            } else {
                pics+=`<div class="col p-2px imgViewer" id="${id}"></div>`;
                generates[j].push(i);
            }
        }
        if (pics=="") { 
            pics="No illustration generated yet";
        } else {
            pics="<div id='style"+i+"' class='row'>"+pics+"</div>";
        }
        styles+=`
            <div class="style-item" id="style-${i}">
                <div class="titre-style fs-5 font-weight-bold">${app.styles[i]}</div>
                <div class="row row-cols-auto mb-1">${pics}</div>
            </div>
        `
    }
    let presets="";
    for (let i=0; i<app.config["style-illustrations"].length; i++) { 
        let preset=app.config["style-illustrations"][i];
        let btn=`
         <button type="button" class="btn btn-sm btn-primary display-inline m-1 p-0 px-1 fs-12px" onclick="generatePresetStyleIllustration(${i}, '${secure(preset.name)}', [${generates[i].toString()}])">
        Generate illustrations for ${generates[i].length} styles that don't have it yet
        </button>
        <br>`
        if (generates[i].length==0) {btn="";}
        let title=secure("Grid view of "+app.styles.length+" styles for the ["+preset.name+" - Prompt= "+preset.metadata.Prompt+"]");

        /* Check if model exists in models list or replace it */
        let htmlModel="";
        let checkModel=checkModelExists(preset.metadata["Base Model"]);
        if (checkModel===true) {
            htmlModel=""+secure(preset.metadata["Base Model"].replace(".safetensors",""))
        } else {
            app.config["style-illustrations"][i].metadata["Alternative Model"]=checkModel           
            htmlModel=`<span class="badge bg-warning">${secure(preset.metadata["Base Model"].replace(".safetensors",""))} not found</span><br>
            ${secure(checkModel.replace(".safetensors",""))}`
        }

        presets+=`            
            <td class="fs-13px" style="width: ${100/app.config["style-illustrations"].length}%">                    
                    <div class="text-center preset-name">${secure(preset.name)} 
                    <button type="button" class="btn btn-sm btn-success display-inline m-1 p-0 px-1 fs-12px" onclick="gridViewIllustration('styles', '${secure(preset.name)}', 6, '${title}')">Grid view</button>
                    </div>
                <div class="text-prompt">${secure(preset.metadata.Prompt)} </div>
                <div class="preset-param">Seed: ${secure(preset.metadata.Seed)} </div>
                <div  class="preset-param">${htmlModel} </div>
                <div class="text-center">
                    ${btn}
                    <button type="button" class="btn btn-sm btn-danger display-inline m-1 p-0 px-1 fs-12px" onclick="generatePresetStyleIllustration(${i}, '${secure(preset.name)}', 'all')">Regenerate all</button>

                </div>
            </td>
        `
    }

    form.html(`
    <div class="container p-0 m-0">
        <h2>Your Fooocus installation gets ${app.styles.length} styles</h2>
        <div class="">Here is the list of illustration presets that can be generated with your Fooocus installation for each style.</div>
        <div class="text-help">You can edit/modify/add the list of presets in the <code>config.json</code> file in the FoooXus app folder. <button type="button" class="btn btn-sm btn-primary py-0 m-0" onclick="viewHelpConfigPreset()">View help about Presets</button></div>
        <table class="table">
        <tbody>
        <tr>
            ${presets}
        </tr>
        </tbody>
        </table>
        <div class="row mt-2">
            <div class="container p-0">
                <div class="mb-1 row">
                    
                    <div class="col"><b>Styles in your Fooocus folder</b></div>
                    <div  class="col"><input type="search" placeholder="Filter styles by name" class="form-control" id="filter-styles" name="filter-styles"  onkeyup="filterStyles(this.value)" onsearch="filterStyles(this.value)"> </div>
                    <div  class="col"s><span id="filter-nb-styles"></span></div>

                </div>
                <div class="mb-1">
                    ${styles}
                </div>
            </div>
        </div>
    </div>
    `);

    $("div#app").append(form);
    setTimeout(function() {madeImgEnlargeable()}, 100);

}


/* Modal of model/style illustrations */
function adjustGridModal(delta) {
    let cols=parseInt($("div#grid-modal").attr("data-cols"))
    let cols2=cols+delta;
    if ((cols2>=1)&&(cols2<=12)) {
        $("div#grid-modal").attr("data-cols", cols2).removeClass(`row-cols-${cols}`).addClass(`row-cols-${cols2}`)
    }
}

/* Filter the images in grid view by name */
function filterGridView(val, images, n) {
    val=val.toLowerCase().trim();
    let nb=0;
    if (val=="") {
        $("div.image-grid-view").removeClass("d-none");
        nb=n;
    } else {
        for (let i=0; i<images.length; i++) {
            if (images[i].toLowerCase().includes(val)) {
                $("div#image-grid-view-"+i).removeClass("d-none");
                nb++;
            } else {
                $("div#image-grid-view-"+i).addClass("d-none");
            }
        }
    }   
    $("span#filter-nb-grid").html(nb+" / "+n+" images found");

}

function gridViewIllustration(items, name, cols=5, desc="") {
    let illustrations=app.illustrations[items];
    let names=[], item="", images=[], nb=0;
    if (items=="models") {names=app.models;  item="MODEL";}
    if (items=="styles") {names=app.styles;  item="STYLE";}
    if (items=="loras")  {names=app.loras;   item="LORA";}

    let html=`<div id="grid-modal" data-cols="${cols}" class='row row-cols-${cols}'>`;
    for (let i=0; i<illustrations.length; i++) {
        if (illustrations[i].endsWith("_"+name+".jpg")) {
            let title=illustrations[i];
            for (let j=0; j<names.length; j++) {
                if (secureFile(names[j].replace(".safetensors",""))+"_"+name+".jpg"==illustrations[i]) {
                    title=secure(names[j].replace(".safetensors",""));
                    images[i]=title;
                    nb++;
                    break;
                }
            }
            html+=`
            <div class="col p-2px imgViewerGrid image-grid-view" id="image-grid-view-${i}">
            <div class="image-container">
                <img src="${app.illustrationsFolder}/${items}/${illustrations[i]}" loading="lazy" class="responsive thumbnail img-enlargeable" title="${item+": "+title+" PRESET: "+secure(name)}">
                <span class="text-center fs-12px image-title">${title}</span>
            </div>
            </div>`;
        }
    }
    html+="</div>";

    if (desc=="") {
        desc=`Grid view of all ${names.length} ${items}`
    }

    new jBox('Modal', {
        title:
        `<div class="row p-0 m-0 pb-1 font-size-bold" style="background-color:#000; font-weight: bold;">
        <div class="col">${desc}</div>
        <div class="col">
            <button type="button" class="btn btn-sm btn-primary mb-1" onclick="adjustGridModal(-1)">Less columns</button>
            <button type="button" class="btn btn-sm btn-primary mb-1" onclick="adjustGridModal(1)">More columns</button>
        </div>
        <div class="col">
            <input type="search" class="form-control d-inline" onsearch="filterGridView(this.value, ['${images.join("','")}'], ${nb})" onkeyup="filterGridView(this.value,  ['${images.join("','")}'], ${nb})" placeholder="Filter images by name"> 
            <span id="filter-nb-grid"></span>
        </div>
        </div>`,
        theme: "TooltipDark",
        content: html,
        blockScroll: true,
        overlay: true,
        closeOnEsc: true,
        closeOnClick: false,
        closeButton: true,
        fixed: true,
    }).open();

    setTimeout(function() {madeImgEnlargeable(), 200})
}



function filterStyles(val) {
    val=val.toLowerCase().trim();
    let nb=0;
    if (val=="") {
        $("div.style-item").show();
        nb=app.styles.length;
    }   else {    
        for (let i=0; i<app.styles.length; i++) {
            if (app.styles[i].toLowerCase().includes(val)) {
                $("div#style-"+i).show();
                nb++;
            } else {  
                $("div#style-"+i).hide();
            }
        }
    }   
    $("span#filter-nb-styles").html(nb+" / "+app.styles.length+" styles found");
}   


function filterModels(val) {
    val=val.toLowerCase().trim();
    let nb=0;
    if (val=="") {
        $("div.model-item").show();
        nb=app.models.length;
    }   else {    
        for (let i=0; i<app.models.length; i++) {
            if (app.models[i].toLowerCase().includes(val)) {
                $("div#model-"+i).show();
                nb++;
            } else {  
                $("div#model-"+i).hide();
            }
        }
    }   
    $("span#filter-nb-models").html(nb+" / "+app.models.length+" models found");
}   
function filterLoras(val) {
    val=val.toLowerCase().trim();
    let nb=0;
    if (val=="") {
        $("div.lora-item").show();
        nb=app.loras.length;
    }   else {    
        for (let i=0; i<app.loras.length; i++) {
            if (app.loras[i].toLowerCase().includes(val)) {
                $("div#lora-"+i).show();
                nb++;
            } else {  
                $("div#lora-"+i).hide();
            }
        }
    }   
    $("span#filter-nb-loras").html(nb+" / "+app.loras.length+" loras found");
}   





/* After app is ready: generation of UI */
function makeAppAPI() {
    if (!app.ready) return;

    activateMenu("menu-api");

    let work=false;

    if (!work) {

        $("div#app").html(`<h2>This form is not ready yet <i class="fa-solid fa-person-digging"></i></h2>
        
        <p><p>In this form, you will generate images from a prompt with variations of one or more parameters (like Guidance value, Loras, refiner, styles, ...)</p>
        
        `);
        return true;
 
    }



    $("div#app").html("");

    var form=$("<form>").attr("id", "form-app");

    var models="";
    for (var i=0; i<app.models.length; i++) {
        models+=`<div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="model-${i}">
            <label class="form-check-label" for="model-${i}"  onclick="resetProcess()">
                ${app.models[i].replace(".safetensors", "")}
            </label>
            </div>
        `
    }

    let selectRatio=`<select name="ratio" id="ratio"  class="form-select"  onchange="resetProcess()">`;
    for (let i=0; i<app.ratios.length; i++) selectRatio+=`<option value="${app.ratios[i]}">${app.ratios[i]}</option>`;
    selectRatio+=`</select>`;

    let selectStyle="", selectRefiner="", selectModel="";

    form.html(`
    <div class="container p-0 m-0">
        <h2>Fooocus App. Working with API</h2>
        <div class="row">
            <div class="col-6">
                <div class="mb-1">
                    <label for="prompt" class="form-label">Prompt</label>
                    <input type="text" class="form-control" id="prompt" name="prompt" onchange="resetProcess()">
                    <div class="form-text">Type your prompt to describe your image.</div>
                </div>
                <div class="mb-1">
                    <label for="negativeprompt" class="form-label">Negative Prompt</label>
                    <input type="text" class="form-control" id="negativeprompt" name="negativeprompt" onchange="resetProcess()">
                    <div class="form-text">Type your negative prompt.</div>
                </div>
                <div class="mb-1">
                    <label for="seed" class="form-label">Seed</label>
                    <input type="text" class="form-control" id="seed" name="seed" onchange="resetProcess()">
                    <div class="form-text">Enter a numeric seed. Keep empty if you want Foooxus adds a seed.</div>
                </div>
                <div class="mb-1">
                    <label for="ratio" class="form-label">Aspect Ratio (width × height)</label>
                    ${selectRatio}
                    <div class="form-text">Choose an image format.</div>
                </div>
                <div class="mb-1">
                    <label for="performance" class="form-label">Performance level</label>
                    <select name="performance" class="form-select" onchange="resetProcess()">
                        <option value="Speed">Speed</option>
                        <option value="Quality">Quality</option>
                        <option value="Extreme Speed">Extreme Speed</option>
                    </select>               
                </div>
                <div class="mb-1">
                    <label for="styles" class="form-label">Styles</label>
                    ${selectStyle}
                    <div class="form-text">Choose style.</div>
                </div>
                <div class="mb-1">
                    <label for="refiner" class="form-label">Refiner</label>
                    ${selectRefiner}
                    <div class="form-text">Choose style.</div>
                </div>
                <div class="mb-1">
                    <label for="refinerSwitch" class="form-label">Refiner Switch</label>
                    <input type="text" class="form-control" id="refinerSwitch" name="refinerSwitch" onchange="resetProcess()">
                    <div class="form-text">Intensity of refiner.</div>
                </div>


                <div class="mb-1">
                    
                    <div class="row justify-content-between">
                        <div class="col-auto">
                            <label for="guidance" class="form-label">Guidance Scale </label>
                        </div>
                        <div class="col-auto">
                            <input type="checkbox" name="guidance-variation" id="guidance-variation" value="0"> <label for="guidance-variation" class="form-label">Generate variations</label>
                        </div>
                    </div>

                    <input type="text" class="form-control" id="guidance" name="guidance" onchange="resetProcess()">
                    <div class="form-text">Higher value means style is cleaner, vivider, and more artistic.</div>
                </div>

                <div class="mb-1">
                    <label for="sharpness" class="form-label">Image Sharpness</label>
                    <input type="text" class="form-control" id="sharpness" name="sharpness" onchange="resetProcess()">
                    <div class="form-text">Higher value means image and texture are sharper.</div>
                </div>

                <div class="mb-1">
                    <label for="positive" class="form-label">Positive ADM</label>
                    <input type="text" class="form-control" id="positive" name="positive" onchange="resetProcess()">
                    <div class="form-text">Positive ADM Guidance Scaler.</div>
                </div>
                <div class="mb-1">
                    <label for="negative" class="form-label">Negative ADM</label>
                    <input type="text" class="form-control" id="negative" name="negative" onchange="resetProcess()">
                    <div class="form-text">Negative ADM Guidance Scaler.</div>
                </div>
                <div class="mb-1">
                    <label for="step" class="form-label">End Step ADM</label>
                    <input type="text" class="form-control" id="step" name="step" onchange="resetProcess()">
                    <div class="form-text">ADM Guidance End At Step.</div>
                </div>


                <button id="btn-process" type="button" class="btn btn-primary" onclick="process(this.form)" data-preprocess="0">Preprocessing call</button>
            </div>
            <div class="col-6">
                <div class="mb-1">
                    <label for="prompt" class="form-label">Models in your Fooocus folder. <button type="button" class="btn btn-sm btn-secondary" onclick="return checkAllModels(true)">Check all</button> <button type="button"  class="btn btn-sm btn-secondary" onclick="return checkAllModels(false)">Uncheck all</button></label>
                    ${models}
                </div>
            </div>
        </div>
    </div>
    
    
    `);


    $("div#app").append(form);
}

/* Reset preprocess button when user change prompt, seed, quality, models, ... */
function resetProcess() {
    $("button#btn-process").attr("data-preprocess", "0")
    $("button#btn-process").html("Preprocessing call");
}  


/* Generates all the JSON to call with API */
function process(f) {

    if ($("button#btn-process").attr("data-preprocess")=="0") {

        
        var jsons=[];
        app.jsons=jsons;

        var prompt = f.prompt.value.trim();
        if (prompt=="") {  
            prompt="A cat in the kitchen";
            f.prompt.value=prompt;
        }

        var seed = f.seed.value.trim();
        if (seed=="") {  
            seed=314159;
            f.seed.value=seed;
        }
        var performance = f.performance.options[f.performance.selectedIndex].value.trim();

        var models = [];
        for (var i=0; i<app.models.length; i++) {
            if (f["model-"+i].checked) {
                models.push(app.models[i]);
            }
        }
        if (models.length==0) {
            new jBox('Notice', {
                content: "You must select at least one model",
                color: 'red'
            });
            return false;
        }

        for (let i=0; i<models.length; i++) {
            jsons[i]=JSON.parse(JSON.stringify(metadataBase));
            jsons[i].Seed=seed;
            jsons[i].Prompt=prompt;
            jsons[i]["Negative Prompt"]="";
            jsons[i]["Guidance Scale"]=4.0000;
            jsons[i].Sharpness=2.0000;
            jsons[i].Styles=[];
            jsons[i].Performance=performance;
            jsons[i]["Base Model"]=models[i];        
        }

        app.jsons=jsons;
        console.log(jsons);

        $("button#btn-process").attr("data-preprocess", "1")
        $("button#btn-process").html("Send "+jsons.length+" image"+(jsons.length>1?"s":"")+" to API");
       

    } else {
        new jBox('Notice', {
            content: "Sending image generation to API",
            color: 'green'
          });

        launchGeneration();  
    }
}




/* Add the app.jsons to app.calls and launch the generation if necessary */
function launchGeneration(callback=function() {}, error=function() {}) {
    var jsons=app.jsons;
    
    if (jsons.length==0) {
        /* Nothing new to launch */
        return false;
    }
    console.log("launchGeneration() called")

    for (let i=0; i<jsons.length; i++) {
        let uuid = generateUID(i+jsons[i].toString());
        if (jsons[i]["Alternative Model"]!="") jsons[i]["Base Model"]=jsons[i]["Alternative Model"]
        app.calls.push(new Call(jsons[i], uuid));
    }

    if (app.activeCall==-1) {
        app.activeCall=0;
    }
    if (!app.generating) {
        sendActiveCall(callback, error);
    }

}




/* Send the next active call to API */
function sendActiveCall(callback=function() {}, error=function() {}) {
    if (app.activeCall==-1) {
        app.generating=false
        return false;
    }

    app.generating=true;
    console.log("generateImage("+app.activeCall+") called uid="+app.calls[app.activeCall].id+" sent to FoooXus")
    app.calls[app.activeCall].calledTime=performance.now();
    $.ajax({
        url: "/ajax/generateImage",
        dataType: "json",
        method: "POST",
        data: {  // Add parameters here
            metadata: JSON.stringify(app.calls[app.activeCall].metadata),
            uid: app.calls[app.activeCall].id,
        },
        success: function (data) {
            console.log("generateImage loaded")
            console.log(data)   
            if ((data.ajax)&&(!data.error)&&(data.image)) {
                console.log("generateImage OK")
                app.calls[app.activeCall].image=data.image;
                app.calls[app.activeCall].endTime=performance.now();
                app.calls[app.activeCall].status=true;
                app.generating=false
                app.activeCall++;
                new jBox('Notice', {
                    content: "A new image has been generated in "+Math.round(data.elapsed_time/1000)+" sec<br><img src='"+data.name+"' class='newImageNotice'><br>Prompt: "+secure(data.metadata.Prompt)+"<br>Model: "+secure(data.metadata["Base Model"] )+"<br>Seed: "+secure(data.metadata.Seed)+"<br>Performance: "+secure(data.metadata.Performance)+"<br>Sharpness: "+secure(data.metadata.Sharpness)+"<br>Guidance: "+secure(data.metadata["Guidance Scale"] )+"<br>Styles: "+secure(data.metadata.Styles)
                });    
                if (app.activeCall<app.calls.length) {
                    sendActiveCall(callback, error);
                } 
                getIllustrations();
                callback(data);
            } else {
                console.log("generateImage ERROR")
                app.calls[app.activeCall].error=data.error;
                app.calls[app.activeCall].endTime=performance.now();
                app.calls[app.activeCall].status=false;
                app.generating=false
                app.activeCall++;
                new jBox('Notice', {
                    content: "One image was not generated: Error in Fooocus",
                    color:"red"
                });
                if (app.activeCall<app.calls.length) {
                    sendActiveCall(callback, error);
                } 
                error(data);
            }
        },
        error: function(evt) {
            console.log("generateImage not found")
            error();
        }
    });
}





/* Call is an object that contains all the information about a call to API */
class Call {
    constructor(json, id, batchID=0) {
        this.batchID=batchID;
        this.metadata=json;
        this.id=id;
        this.insertTime=performance.now();
        this.calledTime=0;
        this.endTime=0;
        this.status=0;
        this.image=null;
        this.error=null;
    }
}

/* Batch is an object that contains all the information about a set of generated images */
class Batch {
    constructor(uid, name, variations){
        this.uid=uid;
        this.name=name;
        this.variations=variations; /* An array of all the metadata items that varies in the batch */
    }
}

/* Check if model exists in Fooocus install folder */
function checkModelExists(model) {
    if (app.models.includes(model)) return true;

    let possibilities=["juggernautXL_v8Rundiffusion.safetensors", "juggernautXL_version6Rundiffusion.safetensors", app.models[0]]
    for (let i=0; i< possibilities.length; i++) {
        if (app.models.includes(possibilities[i])) return possibilities[i];
    }

    return newModel
}

/* Update the initial display of the app */
function showDeviceInfo() {
    if (!app.device.detected) {
        $("div#hardware").html("hardware is not detected");
        return "";
    }
    let cpu=app.device.cpu_name.replace("Intel(R) Core(TM) i", "i").replace("Intel(R) Xeon(R) CPU", "Xeon").replace("AMD Ryzen", "Ryzen").replace("AMD EPYC", "EPYC").replace("CPU", "").replace("Processor", "");
    cpu=cpu.replace(/[0-9]*-Core/gi, "").trim();
    cpu+=" "+app.device.cpu_threads+"-threads";
    cpu+=" @"+formatHz(app.device.cpu_freq);
    let hddFree=formatBytes(app.device.hdd_free, 1);
    let hddTotal=formatBytes(app.device.hdd_total,1);
    let hddPct=(100*app.device.hdd_free/app.device.hdd_total).toFixed(1);
    let ram=formatBytes(app.device.ram_installed, 0);
    let gpu="Unknown";
    if (app.device.gpus.length>0) { 
        if (app.device.gpus[0].name!="") {
            gpu=app.device.gpus[0].name.replace("NVIDIA GeForce", "").replace("AMD Radeon", "").trim(); 
            gpu+=" ("+formatBytes(app.device.gpus[0].memoryTotal*1024*1024, 1)+")";
        }
    }
    let hardware=`
    <i class="bi bi-cpu-fill"></i> ${secure(cpu)} <br>
    <i class="bi bi-memory"></i> RAM ${secure(ram)} <br>
    <i class="bi bi-gpu-card"></i> ${secure(gpu)} <br>
    <i class="bi bi-hdd-fill"></i> HDD ${secure(hddFree)} free (${hddPct}%)/ ${secure(hddTotal)} <br>
    `;

    $("div#hardware").html(hardware);

}

function makeAppHelp() {
    if (!app.ready) return;
    activateMenu("menu-help");
    $("div#help").show().removeClass("d-none");
}

/* Update display makeAppQueue */
function updateQueue() {
    if (app.activeMenu=="menu-queue") {
        /* Save vertical scroll position */
        let scrollPosition = window.scrollY;
        /* Refresh list */
        makeAppQueue();
        /* Restore scroll position */
        window.scrollTo(0, scrollPosition)
    }    
}

function clearQueue() {
    console.log("clearQueue()");
    new jBox("Confirm", {
        confirmButton: "Clear queue",
        cancelButton: "Cancel",
        content: "Do you really want clear queue?",
        blockScroll: false,
        confirm: function () {
            sendCancel();
            var n = app.calls.length;
            for (let i=0; i<n; i++) {
                if (app.calls[i].calledTime==0) {
                    app.calls.splice(i, 1);
                    if (i>0) i--;
                    n = app.calls.length;
                }
           }            
		}
    }).open();
}

function makeAppQueue() {
    if (!app.ready) return;

    activateMenu("menu-queue");

    let queues=[];
    let dones=[];


    for (let i=0; i<app.calls.length; i++) {
        let call=app.calls[i]
        if (call.endTime==0) {
            queues.push(call);
        } else {
            dones.push(call);
        }
    }

    let queue="";
    if (queues.length==0) {
        queue="<h2>No work in queue</h2>";
    } else {
        if (queues.length==1) {
            queue="<br><br><h2>You have a work still in progess. Fooocus will stop it soon.</h2>";
        } else {
            queue="<h2>You have "+queues.length+" works in queue</h2>";
            queue+=`<div id="divClearQueue">Works are in progress... <button type="button" class="btn btn-warning" id="btnClearQueue" onclick="clearQueue()">Clear queue</button></div>`;
        }


        queue+=`<table class='table'>
            <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">Details</th>
            <th scope="col">Status</th>
            </tr>
        </thead>
        <tbody>
        `;

        for (let i=0; i<queues.length; i++) {
            let work=queues[i];
            let status="<i class='fa-solid fa-hourglass-start'></i>";
            if (work.calledTime>0) {
                status='<i class="fa-solid fa-person-running"></i> '+ Math.round((performance.now()-work.calledTime)/1000)+" seconds";
            }
            queue+=`<tr class="work-item">
                <td>${i+1}</td>
                <td>${work.metadata.desc}</td>
                <td class="work-delay">${status}</td>
            </tr>`;
        }
        queue+="</tbody></table>";       
    }

    let done=""
    if (dones.length==0) {
        done="<h2>No work done</h2>"
    } else {
        done="<h2>You have "+dones.length+" work"+(dones.length>1?"s":"")+" done</h2>";
        
        done+=`<table class='table'>
            <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">Details</th>
            <th scope="col">Duration</th>
            </tr>
        </thead>
        <tbody>
        `;
        for (let i=0; i<dones.length; i++) {
            let work=dones[i];
            let sec=Math.round((work.endTime-work.calledTime)/1000);
            let status='<i class="fa-regular fa-clock"></i> '+ sec+" second"+(sec>1?"s":"");
            done+=`<tr class="work-item">
                <td>${i+1}</td>
                <td>${work.metadata.desc}</td>
                <td class="work-delay">${status}</td>
            </tr>`;
        }
        done+="</tbody></table>";       
    }


    let html=`
    <form class="form-app">
        <div class="container p-0 m-0">
       

        ${queue}

        ${done}
        
        <div class="alert alert-dark" role="alert">    
            <p>Remember that queue is stored and processed in this browser App. </p>
            <p><b>If you close or reload this page, queue is lost!</b></p>
        </div>

        </div>
    </form>`;

    $("div#app").html(html);
}


function updateStep(step) {
    console.log("updateStep("+step+") called")
    app.step=step;
    updateHeader();
    $("#button-step"+step).removeClass("btn-secondary").addClass("btn-primary");
    $("#progress-bar-step").css("width", ((step-1)*33)+"%");
    let label = "Initialisation";
    if (step==1) {
        console.log("STEP INIT")
        label = "Initialisation <i class='fas fa-spinner fa-spin'></i>";
    } else if (step==2) {
        label = "Connection to FoooXus <i class='fas fa-spinner fa-spin'></i>";
    } else if (step==3) {
        app.foooxusConnection=true;
        label = "Getting Device informations <i class='fas fa-cog  fa-spin'></i>";
    } else if (step==4) {
        app.fooocusConnection=true;
        label = "Connection to Fooocus API <i class='fas fa-spinner fa-spin'></i>"; 
    }
    $("#label-step").html(label);
    if (step>=3) { displayConnectionFoooxus() }
    if (step>=4) { displayConnections() }
    if (step==5) {
        $("#label-step").html("FoooXus App Ready: it is your turn !");
        if (app.config.versions.PyInstaller) {
            $("#aboutApp").html("FoooXus V"+app.config.FOOOXUS_RELEASE+" standalone foooxus.exe on "+app.config.versions.OS)
        } else {
            $("#aboutApp").html("FoooXus V"+app.config.FOOOXUS_RELEASE+" - Python "+app.config.versions.python+" running on "+app.config.versions.OS)
        }

        setInterval(function() {
            updateHeader();
            updateQueue();
        }, 500);
        setInterval(function() {
            pingAll();
        }, 2000);

        
    }
}


function getDeviceInfo(callback=function() {}, error=function() {}) {
    $.ajax({
        url: "/ajax/getDeviceInfo",
        dataType: "json",
        method: "POST",
        success: function (data) {
            console.log("getDeviceInfo loaded")
            console.log(data)   
            app.device = data
            callback();
        },
        error: function(evt) {
            console.log("getDeviceInfo not found")
            error();
        }
    });
}


/* Get config.txt or config.json is well formated */
function checkConfig(callback=function() {}, error=function() {}) {
    $.ajax({
        url: "/ajax/checkConfig",
        dataType: "json",
        method: "POST",
        success: function (data) {
            console.log("config.json loaded")
            console.log(data)   
            app.config = data;
            callback();
        },
        error: function(evt) {
            console.log("config.json not found");
            error();
        }
    });
}

/* Ping to flask server */
function pingFoooxus(callback=function() {}, error=function() {}) {
    app.pingFoooxus = now();
    $.ajax({
        url: "/ajax/pingFoooxus",
        dataType: "json",
        method: "POST",
        success: function (data) {
            if (data.ping) {
                if (app.config===false) app.config=data.config;
                app.lastPingFoooxusOk = now();
                app.nbPingFoooxus++;
                callback();
            } else {
                error();
            }
        },
        error: function(evt) {
            console.log("Ajax error")
            console.log(evt);
            error();
        }
    });
}


function pingFooocus(callback=function() {}, error=function() {}) {
    /* Check if Fooocus is reachable via API */
    app.pingFooocus = now();
    $.ajax({
        url: "/ajax/pingFooocus",
        dataType: "json",
        method: "POST",
        success: function (data) {
            if (data.ping) {
                app.lastPingFooocusOk = now();
                app.nbPingFooocus++;
                let url=data.fooocusUrl.replace("http://", "").replace("https://", "");
                app.fooocusUrl=url;
                app.fooocusHost=url.split(":")[0];
                app.fooocusPort=url.split(":")[1];
                callback();
            } else {
                console.log("pingFooocus ERROR");
                error();
            }
        },
        error: function(evt) {
            console.log("Ajax error")
            console.log(evt);
            error();
        }
    });
}


function sendCancel(callback=function() {}, error=function() {}) {
    /* cancel Queue */
    $.ajax({
        url: "/ajax/sendCancel",
        dataType: "json",
        method: "POST",
        success: function (data) {
            if (data.ajax) {
                console.log("sendCancel to Fooocus OK")
            } else {
                console.log("sendCancel ERROR");
                error();
            }
        },
        error: function(evt) {
            console.log("Ajax sendCancel error")
            console.log(evt);
            error();
        }
    });
}



function getLoras(callback=function() {}, error=function() {}) {
    /* Call API to get models list */
    $.ajax({
        url: "/ajax/getLoras",
        dataType: "json",
        method: "POST",
        success: function (data) {
            console.log("getLoras loaded")
            console.log(data)
            if (data.loras) {
                console.log("getLoras OK")
                app.loras = data.loras;
                callback();
            } else {
                console.log("getLoras ERROR")
                error();
            }
        },
        error: function(evt) {
            console.log("getLoras not found")
            error();
        }
    });
}

function getModels(callback=function() {}, error=function() {}) {
    /* Call API to get models list */
    $.ajax({
        url: "/ajax/getModels",
        dataType: "json",
        method: "POST",
        success: function (data) {
            console.log("getModels loaded")
            console.log(data)
            if (data.models) {
                console.log("getModels OK")
                app.models = data.models;
                callback();
            } else {
                console.log("getModels ERROR")
                error();
            }
        },
        error: function(evt) {
            console.log("getModels not found")
            error();
        }
    });
}

function getStyles(callback=function() {}, error=function() {}) {
    /* Call API to get models list */
    $.ajax({
        url: "/ajax/getStyles",
        dataType: "json",
        method: "POST",
        success: function (data) {
            console.log("getStyles loaded")
            console.log(data)
            if (data.styles) {
                console.log("getStyles OK")
                app.styles = data.styles;
                callback();
            } else {
                console.log("getStyles ERROR")
                error();
            }
        },
        error: function(evt) {
            console.log("getStyles not found")
            error();
        }
    });
}


/* Get all Illustrations from the illustrations folder */
function getIllustrations(callback=function() {}, error=function() {}) {
    $.ajax({
        url: "/ajax/getIllustrations",
        dataType: "json",
        method: "POST",
        success: function (data) {
            console.log("getIllustrations loaded")
            console.log(data)
            if (data.illustrations) {
                console.log("getIllustrations OK")
                app.illustrations.models = data.illustrations.models;
                app.illustrations.styles = data.illustrations.styles;
                app.illustrations.loras = data.illustrations.loras;
                app.illustrations.lastCheck=performance.now();
                callback();
            } else {
                console.log("getIllustrations ERROR")
                error();
            }
        },
        error: function(evt) {
            console.log("getIllustrations not found")
            error();
        }
    });
}

/* Add Zoom image on click */
function madeImgEnlargeable(mode="illustration") {
    $('img.img-enlargeable').removeClass("img-enlargeable").addClass('img-enlargeabled').css('cursor', 'zoom-in').on('mouseover', function(e) {
        clicktoenlarge=$('<div>').css({
          position: 'absolute',
          top: $(e.currentTarget).offset().top+'px',
          left: $(e.currentTarget).offset().left+'px',
          backgroundColor: '#000',
          color: '#fff',
          paddingLeft: '3px',
          paddingRight: '3px',
          fontSize: '13px',
          fontWeight: 'bold',
          fontStyle: 'italic',
          margin: '2px',
          borderRadius: '2px'
        }).html('Click to enlarge').appendTo('body');
      }).on('mouseout', function(e) {
        clicktoenlarge.remove();
      }).click(function() {
        var src = $(this).attr('src'), legende = $(this).attr('title'), modal;
        var width=parseInt(100*$(this).width()/$(window).width())+'%';
        var height=parseInt(100*$(this).width()/$(window).width())+'%';
        var top=parseInt($(this).offset().top-$(window).scrollTop());
        var left=parseInt($(this).offset().left-$(window).scrollLeft());
  
        function removeModal() {
          modal.removeClass('scale-up-center').animate({
            width: width,
            height: height,
            top: top,
            left: left, 
            opacity:0
          }, 200, function() {
            modal.remove();
          });
          $('body').off('keyup.modal-close');
        }
        modal = $('<div id=\"modal-image\">').css({
          background: 'RGBA(0,0,0,.8) url(' + src + ') no-repeat center',
          backgroundSize: 'contain',
          width: width,
          height: height,
          position: 'fixed',
          zIndex: '10000',
          top: top,
          left: left,
          cursor: 'zoom-out',
          opacity: 0
        }).click(function() {
          removeModal();
        }).appendTo('body').animate({
          width: '100%',
          height: '100%',
          top: 0,
          left:0,
          opacity: 1
        }, 200, function() {
        });
        var info=$('<div>').css({
            display: 'none',
            position: 'relative',
            top: '40px',
            left: '0px',
            color: '#ffffff',
            fontSize: '23px',
            fontWeight: 'bold',
            textAlign: 'center',
            textShadow: '-2px 0px 2px #000, 0px 2px 2px #000, 2px 0px 2px #000, 0px -2px 2px #000' 
        }).html(legende).appendTo(modal).fadeIn(600);
      
      

        $("body").on('keyup.modal-close', function(e) {
            if (e.key === 'Escape') {
              removeModal();
            }
        });

    })
}
