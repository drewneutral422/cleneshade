import re
import os
import sys
import importlib.util

class CleneshadeAPI:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.external_keywords = {}
        self.core_keywords = {'conf', 'public', 'class', 'printf', 'if', 'for', 'import', 'while', 'func'}
        self.current_file = ""
        self.current_class = "Main"

    def throw_error(self, error_type, message, line_num=None):
        loc = f"line {line_num}" if line_num else f"({self.current_class})"
        print(f"./{os.path.basename(self.current_file)} {loc}")
        print(f"{error_type}: {message}")
        sys.exit(1)

    # --- ADDED ENTRY POINT ---
    def translate_and_run(self, file_path):
        """Entry point called by interp.py"""
        self.current_file = file_path
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            # Start the execution loop
            self._execute_lines(lines)
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
        except Exception as e:
            self.throw_error("InterpreterError", str(e))

    def load_module(self, module_path):
        try:
            if "." in module_path:
                module_name = module_path.split('.')[-1]
                file_path = module_path.replace('.', '/') + ".py"
            else:
                module_name = module_path
                file_path = module_path + ".py"
            
            if not os.path.exists(file_path): return

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            
            for method_name in dir(mod):
                if not method_name.startswith("__"):
                    attr = getattr(mod, method_name)
                    if callable(attr):
                        self.external_keywords[f"{module_path}.{method_name}"] = attr
        except Exception as e:
            print(f"Module Error: {e}")

    def process_line(self, line, line_num):
        clean_line = line.strip()
        if not clean_line or clean_line in ('{', '}'): return

        if "class" in clean_line and "func" not in clean_line:
            class_match = re.search(r'class\s*\((.*?)\)', clean_line)
            if class_match:
                self.current_class = class_match.group(1).replace("Send ", "").strip()
            return

        conf_match = re.search(r'conf\s*\((.*?)\)\s*as\s*\("(.*?)"\)', clean_line)
        if conf_match:
            var_name = conf_match.group(1).strip()
            val_content = conf_match.group(2)
            if val_content.startswith(">>>"):
                prompt = val_content.replace(">>>", "").lstrip()
                self.variables[var_name] = input(prompt if prompt else ">>> ")
            else:
                self.variables[var_name] = val_content
            return

        if clean_line.startswith("printf"):
            match = re.search(r'printf\s*\(\s*(.*?)\s*\)', clean_line)
            if match:
                raw_val = match.group(1).strip()
                if raw_val.startswith('"') and raw_val.endswith('"'):
                    print(raw_val.strip('"'))
                elif raw_val in self.variables:
                    print(self.variables[raw_val])
                else:
                    if "+" in raw_val:
                        parts = [p.strip().strip('"') if p.strip().startswith('"') else self.variables.get(p.strip(), p.strip()) for p in raw_val.split("+")]
                        print("".join(map(str, parts)))
                    else:
                        self.throw_error("Null", f"'{raw_val}' is not defined.", line_num)
            return

        # Check for function calls: name()
        func_call_match = re.match(r'^([a-zA-Z0-9_]+)\(\)', clean_line)
        if func_call_match:
            func_name = func_call_match.group(1)
            if func_name in self.functions:
                self._execute_lines(self.functions[func_name])
                return

        for key, func in self.external_keywords.items():
            if clean_line.startswith(key):
                arg_match = re.search(r'\((.*?)\)', clean_line)
                args_list = []
                if arg_match and arg_match.group(1).strip():
                    raw_args = arg_match.group(1).split(',')
                    for arg in raw_args:
                        arg = arg.strip()
                        val = self.variables.get(arg, arg.strip('"'))
                        args_list.append(val)
                try:
                    func(*args_list) if args_list else func()
                except Exception as e:
                    self.throw_error("RuntimeError", str(e), line_num)
                return

    def _execute_lines(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            line_num = i + 1
            if not line or line.startswith("//"): 
                i += 1
                continue

            if "public func" in line:
                func_match = re.search(r'func\s*([a-zA-Z0-9_]+)', line)
                if func_match:
                    name = func_match.group(1)
                    block, consumed = self._get_block(lines[i:])
                    self.functions[name] = block
                    i += consumed
                    continue

            while_match = re.search(r'while\s*\(\s*(.*?)\s*\)', line)
            if while_match:
                condition = while_match.group(1)
                block, consumed = self._get_block(lines[i:])
                while self._evaluate(condition):
                    self._execute_lines(block)
                i += consumed
                continue

            for_match = re.search(r'for\s*\(\s*(\d+)\s*\)', line)
            if for_match:
                iterations = int(for_match.group(1))
                block, consumed = self._get_block(lines[i:])
                for _ in range(iterations):
                    self._execute_lines(block)
                i += consumed
                continue

            if_match = re.search(r'if\s*\(\s*(.*?)\s*\)', line)
            if if_match:
                condition = if_match.group(1)
                block, consumed = self._get_block(lines[i:])
                if self._evaluate(condition):
                    self._execute_lines(block)
                i += consumed
                continue

            if line.startswith("import "):
                self.load_module(line.replace("import ", "").strip())
                i += 1
                continue

            self.process_line(line, line_num)
            i += 1

    def _get_block(self, lines_suffix):
        block, depth, consumed = [], 0, 0
        for line in lines_suffix:
            consumed += 1
            if '{' in line: depth += 1
            if depth > 0 and '{' not in line and '}' not in line:
                block.append(line)
            if '}' in line:
                depth -= 1
                if depth == 0: break
        return block, consumed

    def _evaluate(self, condition):
        if " and " in condition:
            parts = condition.split(" and ")
            return all(self._evaluate(p.strip()) for p in parts)
            
        if "==" in condition:
            parts = condition.split("==")
            l_val = self.variables.get(parts[0].strip(), parts[0].strip().strip('"'))
            r_val = self.variables.get(parts[1].strip(), parts[1].strip().strip('"'))
            return str(l_val) == str(r_val)
        
        if "!=" in condition:
            parts = condition.split("!=")
            l_val = self.variables.get(parts[0].strip(), parts[0].strip().strip('"'))
            r_val = self.variables.get(parts[1].strip(), parts[1].strip().strip('"'))
            return str(l_val) != str(r_val)
            
        return False
