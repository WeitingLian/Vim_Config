#!/usr/bin/env python3
"""
ctags_gen.py
Generate ctags using separate filelist and options configuration
Command line interface with argparse
"""

import os
import sys
import re
import logging
import argparse
import subprocess
from pathlib import Path
from typing import List

class CtagsGenerator:
    def __init__(self, filelist_file: str, options_file: str = None, log_file: str = "ctags_generation.log"):
        self.filelist_file = filelist_file
        self.options_file = options_file
        self.log_file = log_file
        self.directories = []
        self.files = []
        self.exclude_patterns = []
        self.ctags_options = []
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def expand_path(self, path: str) -> str:
        """Expand environment variables and resolve path"""
        expanded = os.path.expandvars(path)
        return os.path.abspath(expanded)
    
    def parse_filelist(self) -> bool:
        """Parse the filelist configuration file"""
        self.logger.info(f"Parsing filelist: {self.filelist_file}")
        
        if not os.path.exists(self.filelist_file):
            self.logger.error(f"Filelist not found: {self.filelist_file}")
            return False
            
        current_section = None
        section_handlers = {
            'DIRECTORIES': self.parse_directory_entry,
            'FILES': self.parse_file_entry,
            'EXCLUDE': self.parse_exclude_entry
        }
        
        try:
            with open(self.filelist_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Check for section headers
                    if line.endswith(':'):
                        current_section = line[:-1].upper()
                        self.logger.debug(f"Filelist - Entering section: {current_section}")
                        continue
                    
                    # Process section content
                    if current_section in section_handlers:
                        section_handlers[current_section](line, line_num)
                    else:
                        self.logger.warning(f"Line {line_num}: Unknown section '{current_section}', skipping: {line}")
            
            self.logger.info(f"Filelist parsed: {len(self.directories)} directories, {len(self.files)} files, {len(self.exclude_patterns)} exclude patterns")
            return True
            
        except Exception as e:
            self.logger.error(f"Error parsing filelist: {e}")
            return False
    
    def parse_directory_entry(self, line: str, line_num: int):
        """Parse directory entries from filelist"""
        expanded_path = self.expand_path(line)
        if os.path.isdir(expanded_path):
            self.directories.append(expanded_path)
            self.logger.debug(f"Added directory: {expanded_path}")
        else:
            self.logger.warning(f"Line {line_num}: Directory not found: {expanded_path}")
    
    def parse_file_entry(self, line: str, line_num: int):
        """Parse file entries from filelist"""
        expanded_path = self.expand_path(line)
        if os.path.isfile(expanded_path):
            self.files.append(expanded_path)
            self.logger.debug(f"Added file: {expanded_path}")
        else:
            self.logger.warning(f"Line {line_num}: File not found: {expanded_path}")
    
    def parse_exclude_entry(self, line: str, line_num: int):
        """Parse exclude patterns from filelist"""
        self.exclude_patterns.append(line)
        self.logger.debug(f"Added exclude pattern: {line}")
    
    def parse_options(self) -> bool:
        """Parse the ctags options configuration file"""
        if not self.options_file:
            self.logger.info("No options file specified, using default ctags options")
            # Add some sensible defaults
            self.ctags_options.extend([
                '--languages=SystemVerilog',
                '--fields=+afinSt',
                '--sort=yes'
            ])
            return True
            
        self.logger.info(f"Parsing options: {self.options_file}")
        
        if not os.path.exists(self.options_file):
            self.logger.error(f"Options file not found: {self.options_file}")
            return False
        
        try:
            with open(self.options_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Handle --options reference (load external .ctags files)
                    if line.startswith('--options='):
                        included_file = line.split('=', 1)[1].strip()
                        expanded_include = self.expand_path(included_file)
                        if os.path.isfile(expanded_include):
                            self.logger.info(f"Loading external ctags file: {expanded_include}")
                            self.load_external_ctags_file(expanded_include)
                        else:
                            self.logger.warning(f"External ctags file not found: {expanded_include}")
                        continue
                    
                    # Add to ctags options
                    self.ctags_options.append(line)
                    self.logger.debug(f"Added ctags option: {line}")
            
            self.logger.info(f"Options parsed: {len(self.ctags_options)} ctags options")
            return True
            
        except Exception as e:
            self.logger.error(f"Error parsing options file: {e}")
            return False
    
    def load_external_ctags_file(self, file_path: str):
        """Load options from external .ctags file"""
        # Options that conflict with our -L filelist approach
        conflicting_options = {
            '-R', '--recurse', 
            '-L', '--list-files',
            '--file-list'
        }
        
        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Handle nested --options references
                    if line.startswith('--options='):
                        included_file = line.split('=', 1)[1].strip()
                        expanded_include = self.expand_path(included_file)
                        if os.path.isfile(expanded_include):
                            self.logger.info(f"Loading nested ctags file: {expanded_include}")
                            self.load_external_ctags_file(expanded_include)
                        continue
                    
                    # Skip conflicting options
                    option_word = line.split()[0] if line else ''
                    if option_word in conflicting_options:
                        self.logger.warning(f"Skipping conflicting option from {file_path}: {line}")
                        continue
                    
                    # Add valid option
                    self.ctags_options.append(line)
                    self.logger.debug(f"Added option from external config: {line}")
                    
        except Exception as e:
            self.logger.warning(f"Error reading external ctags file {file_path}: {e}")
    
    def should_exclude(self, path: str) -> bool:
        """Check if path should be excluded based on patterns"""
        for pattern in self.exclude_patterns:
            # Convert wildcard pattern to regex
            regex_pattern = pattern.replace('*', '.*')
            if re.search(regex_pattern, path):
                return True
        return False
    
    def find_systemverilog_files(self) -> List[str]:
        """Find all SystemVerilog files based on filelist configuration"""
        all_files = set()
        sv_extensions = {'.sv', '.svh', '.v', '.vh', '.svi'}
        
        self.logger.info("Searching for SystemVerilog files...")
        
        # Add individual files
        for file_path in self.files:
            if os.path.isfile(file_path):
                all_files.add(file_path)
        
        # Search directories recursively
        for directory in self.directories:
            self.logger.info(f"Searching directory: {directory}")
            try:
                for root, dirs, files in os.walk(directory):
                    # Apply exclude patterns to directories
                    dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d))]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        if (Path(file).suffix.lower() in sv_extensions and 
                            not self.should_exclude(file_path) and
                            os.path.isfile(file_path)):
                            all_files.add(file_path)
                            
            except Exception as e:
                self.logger.error(f"Error searching directory {directory}: {e}")
        
        file_list = sorted(list(all_files))
        self.logger.info(f"Found {len(file_list)} SystemVerilog files")
        return file_list
    
    def generate_file_list(self, file_list: List[str]) -> str:
        """Create temporary file with list of files to process"""
        temp_file = "ctags_processing_list.tmp"
        with open(temp_file, 'w') as f:
            for file_path in file_list:
                f.write(file_path + '\n')
        return temp_file
    
    def run_ctags(self, file_list: List[str]) -> bool:
        """Run ctags command using subprocess - safe for special characters"""
        if not file_list:
            self.logger.error("No files to process")
            return False
        
        self.logger.info("Generating ctags...")
        
        # Create file list
        list_file = self.generate_file_list(file_list)
        
        # Build ctags command
        cmd = ['ctags', '-L', list_file, '-f', 'tags']
        cmd.extend(self.ctags_options)
        
        self.logger.info(f"Running command: {' '.join(cmd)}")
        
        try:
            # Use subprocess to avoid shell interpretation issues
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            stdout, stderr = process.communicate()
            return_code = process.returncode
            
            if return_code == 0:
                self.logger.info("ctags completed successfully")
                if os.path.exists('tags'):
                    with open('tags', 'r') as f:
                        tag_count = sum(1 for _ in f)
                    self.logger.info(f"Generated {tag_count} tags in 'tags' file")
                success = True
            else:
                self.logger.error(f"ctags failed with return code {return_code}")
                if stderr:
                    self.logger.error(f"ctags stderr: {stderr}")
                success = False
                
            # Log output for debugging
            if stdout:
                self.logger.info(f"ctags stdout: {stdout}")
                
        except Exception as e:
            self.logger.error(f"Error running ctags: {e}")
            success = False
        finally:
            # Clean up temporary file
            if os.path.exists(list_file):
                try:
                    os.remove(list_file)
                except OSError:
                    pass
        
        return success
    
    def print_summary(self):
        """Print summary of configuration"""
        self.logger.info("=== Configuration Summary ===")
        self.logger.info("FILELIST:")
        self.logger.info(f"  File: {self.filelist_file}")
        self.logger.info(f"  Directories: {len(self.directories)}")
        for directory in self.directories:
            self.logger.info(f"    - {directory}")
        
        self.logger.info(f"  Files: {len(self.files)}")
        for file_path in self.files:
            self.logger.info(f"    - {file_path}")
        
        self.logger.info(f"  Exclude patterns: {len(self.exclude_patterns)}")
        for pattern in self.exclude_patterns:
            self.logger.info(f"    - {pattern}")
        
        self.logger.info("CTAGS OPTIONS:")
        if self.options_file:
            self.logger.info(f"  Options file: {self.options_file}")
        else:
            self.logger.info("  Options file: (using defaults)")
        self.logger.info(f"  Options count: {len(self.ctags_options)}")
        for option in self.ctags_options[:10]:  # Show first 10 options
            self.logger.info(f"    - {option}")
        if len(self.ctags_options) > 10:
            self.logger.info(f"    ... and {len(self.ctags_options) - 10} more options")
    
    def generate(self) -> bool:
        """Main generation function"""
        self.logger.info("=== Starting ctags generation ===")
        
        # Parse filelist configuration
        if not self.parse_filelist():
            return False
        
        # Parse ctags options
        if not self.parse_options():
            return False
        
        # Print configuration summary
        self.print_summary()
        
        # Find files based on filelist
        file_list = self.find_systemverilog_files()
        
        if not file_list:
            self.logger.error("No SystemVerilog files found to process")
            return False
        
        # Log file list (first 10 files)
        self.logger.info(f"Files to be processed (showing first 10 of {len(file_list)}):")
        for file_path in file_list[:10]:
            self.logger.info(f"  {file_path}")
        if len(file_list) > 10:
            self.logger.info(f"  ... and {len(file_list) - 10} more files")
        
        # Generate tags
        success = self.run_ctags(file_list)
        
        if success:
            self.logger.info("=== ctags generation completed successfully ===")
        else:
            self.logger.error("=== ctags generation failed ===")
        
        return success

def setup_argparse():
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description='Generate ctags for SystemVerilog projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -f filelist.txt
  %(prog)s -f filelist.txt --opt options.txt
  %(prog)s -f filelist.txt --opt options.txt --log generation.log
  %(prog)s -f filelist.txt --log debug.log
        """
    )
    
    parser.add_argument(
        '-f', '--filelist',
        required=True,
        help='Filelist configuration file (required)'
    )
    
    parser.add_argument(
        '--opt', '--options',
        dest='options_file',
        help='ctags options configuration file (optional)'
    )
    
    parser.add_argument(
        '--log',
        default='ctags_generation.log',
        help='Log file path (default: ctags_generation.log)'
    )
    
    return parser

def main():
    """Main function"""
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Validate filelist exists
    if not os.path.exists(args.filelist):
        print(f"ERROR: Filelist not found: {args.filelist}")
        sys.exit(1)
    
    # Validate options file if provided
    if args.options_file and not os.path.exists(args.options_file):
        print(f"ERROR: Options file not found: {args.options_file}")
        sys.exit(1)
    
    print("Starting ctags generation:")
    print(f"  Filelist: {args.filelist}")
    print(f"  Options: {args.options_file if args.options_file else '(default)'}")
    print(f"  Log file: {args.log}")
    print()
    
    generator = CtagsGenerator(args.filelist, args.options_file, args.log)
    success = generator.generate()
    
    if success:
        print("\nctags generation completed successfully")
        print(f"Check {args.log} for detailed information")
    else:
        print("\nctags generation failed")
        print(f"Check {args.log} for error details")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()