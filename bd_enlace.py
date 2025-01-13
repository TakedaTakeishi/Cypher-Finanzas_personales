from queue import Queue
from threading import Thread, Lock
import sqlite3 as sql
from datetime import datetime, timedelta
import controladores.Base_Controlador as bc

class DatabaseBridge:
    def __init__(self):
        self.base = None
        self.cursor = None
        self.current_user = None
        self.queue = Queue()
        self.lock = Lock()
        self.worker_thread = Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def _process_queue(self):
        """Worker thread que procesa las operaciones de base de datos."""
        while True:
            func, args, callback = self.queue.get()
            if func is None:
                break
            try:
                with self.lock:
                    result = func(*args)
                if callback:
                    callback(result)
            except Exception as e:
                print(f"Error en operación de base de datos: {e}")
                if callback:
                    callback(False)
            self.queue.task_done()

    def _connect_user_impl(self, username, password):
        """Implementación real de la conexión de usuario."""
        try:
            if not bc.verificar_BD(username):
                fecha_actual = datetime.now().strftime('%Y-%m-%d')
                self.base, self.cursor = bc.base_Inicializar(1, username, fecha_actual)
            else:
                self.base, self.cursor = bc.base_Inicializar(2, username)
            
            self.current_user = username
            return True
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")
            return False

    def _handle_date_impl(self, date_str):
        """Implementación real del manejo de fechas."""
        try:
            if not self.cursor:
                return False

            fecha_max, id_max = bc.fecha_Max(self.cursor)
            fecha_seleccionada = datetime.strptime(date_str, '%Y-%m-%d').date()
            fecha_maxima = datetime.strptime(fecha_max, '%Y-%m-%d').date()
            
            if fecha_seleccionada > fecha_maxima:
                dias_adicionales = (fecha_seleccionada - fecha_maxima).days
                bc.generarDias(self.base, self.cursor, fecha_max, dias_adicionales)
            return True
        except Exception as e:
            print(f"Error al manejar la selección de fecha: {e}")
            return False

    def _upload_operations_impl(self, operations, selected_date):
        """Implementación real de la subida de operaciones."""
        try:
            if not self.cursor:
                return False

            dia_id = bc.ID_de_fecha(self.cursor, selected_date)

            for op in operations:
                monto = float(op['monto'])
                if op['transaccion'] == 'egreso':
                    monto = -monto

                intervalo = None
                fecha_final = None
                if op['operation_type'] == 'recurrente':
                    intervalo = -1
                    fecha_final = (datetime.strptime(selected_date, '%Y-%m-%d') + 
                                 timedelta(days=365)).strftime('%Y-%m-%d')

                bc.insertOperation(
                    self.base,
                    self.cursor,
                    dia_id,
                    op['concepto'],
                    monto,
                    op['rubro'] if op['rubro'] else None,
                    intervalo,
                    fecha_final
                )

            fecha_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            bc.actualizar_diario(self.base, self.cursor, fecha_obj)
            
            return True
        except Exception as e:
            print(f"Error al subir operaciones: {e}")
            return False

    # Métodos públicos que encolan las operaciones
    def connect_user(self, username, password):
        """Encola la operación de conexión de usuario."""
        result = []
        def callback(success):
            result.append(success)
        self.queue.put((self._connect_user_impl, (username, password), callback))
        self.queue.join()
        return result[0] if result else False

    def handle_date_selection(self, date_str):
        """Encola la operación de manejo de fecha."""
        result = []
        def callback(success):
            result.append(success)
        self.queue.put((self._handle_date_impl, (date_str,), callback))
        self.queue.join()
        return result[0] if result else False

    def upload_operations(self, operations, selected_date):
        """Encola la operación de subida de operaciones."""
        result = []
        def callback(success):
            result.append(success)
        self.queue.put((self._upload_operations_impl, (operations, selected_date), callback))
        self.queue.join()
        return result[0] if result else False

    def close_connection(self):
        """Cierra la conexión y detiene el worker thread."""
        self.queue.put((None, None, None))  # Señal para detener el worker
        if self.worker_thread.is_alive():
            self.worker_thread.join()
        if self.base:
            with self.lock:
                self.base.close()
                self.base = None
                self.cursor = None
                self.current_user = None

    def _get_monthly_data_impl(self):
        """Implementación real de obtener datos mensuales."""
        try:
            if not self.cursor:
                return None
            return bc.obtener_datos_mensuales(self.cursor)
        except Exception as e:
            print(f"Error al obtener datos mensuales: {e}")
            return None

    def _get_category_data_impl(self):
        """Implementación real de obtener datos por categoría."""
        try:
            if not self.cursor:
                return None
            return bc.obtener_datos_categorias(self.cursor)
        except Exception as e:
            print(f"Error al obtener datos por categoría: {e}")
            return None

    def _get_daily_data_impl(self):
        """Implementación real de obtener datos diarios."""
        try:
            if not self.cursor:
                return None
            return bc.obtener_datos_diarios(self.cursor)
        except Exception as e:
            print(f"Error al obtener datos diarios: {e}")
            return None

    def get_monthly_data(self):
        """Encola la operación de obtener datos mensuales."""
        result = [None]
        def callback(data):
            result[0] = data
        self.queue.put((self._get_monthly_data_impl, (), callback))
        self.queue.join()
        return result[0]

    def get_category_data(self):
        """Encola la operación de obtener datos por categoría."""
        result = [None]
        def callback(data):
            result[0] = data
        self.queue.put((self._get_category_data_impl, (), callback))
        self.queue.join()
        return result[0]

    def get_daily_data(self):
        """Encola la operación de obtener datos diarios."""
        result = [None]
        def callback(data):
            result[0] = data
        self.queue.put((self._get_daily_data_impl, (), callback))
        self.queue.join()
        return result[0]