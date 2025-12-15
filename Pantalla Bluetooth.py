// ==============================================================================
// LIBRERÍAS
// ==============================================================================
#include <BluetoothSerial.h>
#include <TFT_eSPI.h>

// ==============================================================================
// INSTANCIAS GLOBALES
// ==============================================================================
// Instancia de Bluetooth
BluetoothSerial SerialBT;

// Instancia de la pantalla TFT 
TFT_eSPI tft = TFT_eSPI();

// ==============================================================================
// VARIABLES GLOBALES DE DATOS
// ==============================================================================
int cpu_usage = 0;
int ram_usage = 0;
int gpu_temp = 0;
bool isConnected = false;

// ==============================================================================
// COLORES
// ==============================================================================
#define BLUE_LIGHT 0x8C1F // Color para el encabezado
#define BLACK_DARK 0x0000 // Negro
#define WHITE_LIGHT 0xFFFF // Blanco
#define TEXT_CPU TFT_GREEN // Verde para CPU
#define TEXT_RAM TFT_YELLOW // Amarillo para RAM
#define TEXT_TEMP TFT_ORANGE // Naranja para TEMP

// ==============================================================================
// FUNCIÓN: Procesa la cadena de datos entrante (ej. "3|79|45")
// ==============================================================================
void processData(String data) {
    // Busca los separadores '|'
    int index1 = data.indexOf('|');
    int index2 = data.lastIndexOf('|');

    // Verifica que haya dos separadores y que el formato sea correcto
    if (index1 != -1 && index2 != -1 && index1 < index2) {
        // 1. Extraer CPU
        String cpuStr = data.substring(0, index1);
        cpu_usage = cpuStr.toInt();

        // 2. Extraer RAM
        String ramStr = data.substring(index1 + 1, index2);
        ram_usage = ramStr.toInt();

        // 3. Extraer GPU/TEMP
        String gpuStr = data.substring(index2 + 1);
        gpu_temp = gpuStr.toInt();
        
        // La conexión está establecida si se reciben datos válidos
        isConnected = true;
    }
}

// ==============================================================================
// FUNCIÓN: Dibuja la interfaz fija (solo se llama una vez)
// ==============================================================================
void drawStaticInterface() {
    tft.fillScreen(BLACK_DARK);
    
    // Título principal
    tft.fillRect(0, 0, tft.width(), 30, BLUE_LIGHT);
    tft.setTextColor(WHITE_LIGHT);
    tft.setTextSize(2); 
    tft.setTextDatum(MC_DATUM); // Centro
    tft.drawString("SYSTEM MONITOR", tft.width() / 2, 15);

    // Etiquetas de datos
    tft.setTextSize(2);
    tft.setTextDatum(TL_DATUM); // Alineación izquierda
    tft.setTextColor(TFT_WHITE);
    
    // Etiquetas fijas
    tft.drawString("CPU USAGE:", 20, 70);
    tft.drawString("RAM USAGE:", 20, 120);
    tft.drawString("GPU/TEMP:", 20, 170);

    // Etiqueta de conexión (inicial)
    tft.setTextSize(1);
    tft.drawString("ESPERANDO CONEXION", 20, tft.height() - 20);
}

// ==============================================================================
// FUNCIÓN: Dibuja los valores dinámicos
// ==============================================================================
void drawDynamicValues() {
    // 1. Limpiar áreas de valores anteriores
    // Esto es crucial para que los números no se superpongan (cubre el área de los 3 valores)
    tft.fillRect(150, 70, 150, 150, BLACK_DARK); 

    // 2. DIBUJAR CPU USAGE
    tft.setTextColor(TEXT_CPU, BLACK_DARK);
    tft.setTextSize(2); 
    tft.setTextDatum(TL_DATUM);
    tft.drawString(String(cpu_usage) + " %", 150, 70);

    // 3. DIBUJAR RAM USAGE
    tft.setTextColor(TEXT_RAM, BLACK_DARK);
    tft.drawString(String(ram_usage) + " %", 150, 120);

    // 4. DIBUJAR GPU/TEMP
    tft.setTextColor(TEXT_TEMP, BLACK_DARK);
    tft.drawString(String(gpu_temp) + " C", 150, 170);

    // 5. Actualizar estado de conexión Bluetooth
    tft.fillRect(20, tft.height() - 20, 200, 20, BLACK_DARK);
    tft.setTextSize(1);
    if (isConnected) {
        tft.setTextColor(TFT_CYAN);
        tft.drawString("CONECTADO", 20, tft.height() - 20);
    } else {
        tft.setTextColor(TFT_RED);
        tft.drawString("ESPERANDO CONEXION", 20, tft.height() - 20);
    }
}

// ==============================================================================
// SETUP
// ==============================================================================
void setup() {
    // Inicialización de la pantalla
    tft.init();
    // Rotación 3 es generalmente la orientación horizontal para TFT 240x320
    tft.setRotation(3); 

    // Inicialización del Bluetooth con un nombre amigable
    SerialBT.begin("Monitor_ESP32"); 

    // Dibuja la interfaz base (estática)
    drawStaticInterface();
}

// ==============================================================================
// LOOP
// ==============================================================================
void loop() {
    // 1. Verificar si hay datos disponibles en el puerto Bluetooth
    if (SerialBT.available()) {
        // Lee la línea completa enviada por Python (termina en '\n')
        String data = SerialBT.readStringUntil('\n'); 
        
        // Procesar la cadena y actualizar las variables globales
        processData(data);
    }
    
    // 2. Dibujar los valores actualizados en la pantalla
    // Esto se hace continuamente para refrescar la información
    drawDynamicValues(); 

    // Pausa para evitar que el ESP32 se sature
    delay(100); 
}
