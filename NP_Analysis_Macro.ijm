// ============================================================
// MACRO: Nanoparticle Analysis from TIF Stack
// Autor: Claude + Usuario
// 
// Flujo:
//   1. Convierte cada slice a 8-bit con auto contraste
//   2. Bandpass FFT (335px - 35px, tolerancia 20%) para eliminar carbono
//   3. Threshold Otsu
//   4. Fill Holes + 2x Dilate
//   5. Particle Analyzer (800px² - Infinity, circ 0.30-1.00)
//   6. Exporta CSV + stack TIF de overlays con ROIs en magenta
//
// Parametros clave:
//   - Pixel size: 0.3 nm/px
//   - Rango NPs: 15-60 nm (~50-200 px de diametro)
//   - Area minima: 800 px² (~16 nm diametro efectivo tras bandpass)
//
// NOTA: El Feret medido puede subestimar ~1-2 nm por el suavizado
//       del bandpass. Validar con medidas manuales en ~20-30 NPs.
// ============================================================

// --- CONFIGURACION ---
var pixelSize      = 0.3;   // nm/pixel
var bandpassLarge  = 335;   // px - elimina estructuras grandes (carbono)
var bandpassSmall  = 35;    // px - elimina ruido fino
var bandpassTol    = 20;    // % tolerancia de direccion
var minArea        = 800;   // px² minimo
var minCirc        = 0.30;  // circularidad minima
var maxCirc        = 1.00;  // circularidad maxima
var nDilate        = 2;     // numero de dilates

// --- INICIO ---
if (nImages == 0) {
    exit("No hay imagenes abiertas. Abre el stack TIF primero.");
}

outputDir = getDirectory("Selecciona carpeta para guardar resultados");
if (outputDir == "") exit("No se selecciono directorio de salida.");

stackID     = getImageID();
stackTitle  = getTitle();
totalSlices = nSlices();

print("\\Clear");
print("=== NP Analysis Macro ===");
print("Stack: " + stackTitle);
print("Total slices: " + totalSlices);
print("Pixel size: " + pixelSize + " nm/px");
print("========================");

// Configurar medidas
run("Set Measurements...", "area perimeter shape feret's redirect=None decimal=4");
run("Set Scale...", "distance=1 known=" + pixelSize + " unit=nm");

// Limpiar resultados previos
if (isOpen("Results"))     { selectWindow("Results");     run("Close"); }
if (isOpen("Summary"))     { selectWindow("Summary");     run("Close"); }
if (isOpen("ROI Manager")) { roiManager("Reset"); }

// Crear stack de overlays vacio RGB del mismo tamaño
selectImage(stackID);
imgW = getWidth();
imgH = getHeight();
newImage("Overlay_Stack", "RGB black", imgW, imgH, totalSlices);
overlayStackID = getImageID();

// setBatchMode OFF para que Flatten funcione con overlays
setBatchMode(false);

// --- BUCLE POR SLICES ---
for (s = 1; s <= totalSlices; s++) {

    // ---- A. Duplicar original para overlay (RGB) ----
    selectImage(stackID);
    setSlice(s);
    run("Duplicate...", "title=orig_" + s);
    origID = getImageID();
    run("Enhance Contrast", "saturated=0.35");
    run("8-bit");
    run("RGB Color");

    // ---- B. Duplicar para procesado ----
    selectImage(stackID);
    setSlice(s);
    run("Duplicate...", "title=proc_" + s);
    procID = getImageID();

    run("Enhance Contrast", "saturated=0.35");
    run("8-bit");

    run("Bandpass Filter...",
        "filter_large=" + bandpassLarge +
        " filter_small=" + bandpassSmall +
        " suppress=None tolerance=" + bandpassTol +
        " autoscale saturate");

    run("Enhance Contrast", "saturated=0.35");
    run("8-bit");

    setAutoThreshold("Otsu");
    run("Convert to Mask");
    run("Fill Holes");
    for (d = 0; d < nDilate; d++) { run("Dilate"); }

    // ---- C. Particle Analyzer -> ROI Manager ----
    roiManager("Reset");
    run("Analyze Particles...",
        "size=" + minArea + "-Infinity" +
        " circularity=" + minCirc + "-" + maxCirc +
        " show=Nothing display exclude include summarize add");

    // ---- D. Dibujar ROIs sobre imagen original ----
    selectImage(origID);
    nROIs = roiManager("count");
    if (nROIs > 0) {
        roiManager("Set Color", "magenta");
        roiManager("Set Line Width", 2);
        roiManager("Show All with labels");
        run("Flatten");
        flatID = getImageID();
    } else {
        selectImage(origID);
        run("Duplicate...", "title=flat_" + s);
        flatID = getImageID();
    }

    // ---- E. Copiar al stack de overlays ----
    selectImage(flatID);
    run("Copy");
    selectImage(overlayStackID);
    setSlice(s);
    run("Paste");
    run("Select None");

    // ---- F. Limpiar ventanas de este slice ----
    selectImage(flatID);  close();
    selectImage(origID);  close();
    selectImage(procID);  close();
    roiManager("Reset");

    if (s % 10 == 0 || s == totalSlices) {
        print("Procesados: " + s + "/" + totalSlices + " slices");
    }
}

// --- GUARDAR ---
selectImage(overlayStackID);
saveAs("Tiff", outputDir + "Overlay_Stack.tif");
print("Guardado: Overlay_Stack.tif");

if (isOpen("Results")) {
    selectWindow("Results");
    saveAs("Results", outputDir + "NP_medidas_individuales.csv");
    print("Guardado: NP_medidas_individuales.csv");
}

if (isOpen("Summary")) {
    selectWindow("Summary");
    saveAs("Results", outputDir + "NP_resumen_por_imagen.csv");
    print("Guardado: NP_resumen_por_imagen.csv");
}

print("========================");
print("ANALISIS COMPLETADO");
print("Resultados en: " + outputDir);
print("========================");

showMessage("Analisis completado",
    "Procesados " + totalSlices + " slices.\n\n" +
    "Archivos generados:\n" +
    "- Overlay_Stack.tif\n" +
    "- NP_medidas_individuales.csv\n" +
    "- NP_resumen_por_imagen.csv\n\n" +
    "RECUERDA: Validar Feret con ~20-30 medidas manuales\n" +
    "para calcular el factor de correccion del bandpass.");
