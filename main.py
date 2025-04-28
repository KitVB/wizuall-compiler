# main.py
import argparse
import sys
import os
import logging

from preprocessor.pdf_extractor import PDFExtractor
from preprocessor.data_formatter import DataFormatter
from scanner.lexer import Lexer
from parser.parser import Parser
from semantics.semantic_analyzer import SemanticAnalyzer
from semantics.code_generator import CodeGenerator
from runtime.executor import RuntimeExecutor

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logger = logging.getLogger('wizuall')
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='WizuAll Compiler')
    parser.add_argument('source_file', help='Path to WizuAll source file')
    parser.add_argument('--data', help='Path to data file (CSV, PDF, etc.)')
    parser.add_argument('--target', choices=['python', 'c', 'r'], 
                        default='python', help='Target language (default: python)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--execute', action='store_true', help='Execute the generated code')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Check if source file exists
        if not os.path.exists(args.source_file):
            logger.error(f"Source file not found: {args.source_file}")
            return 1
        
        # Read source code
        logger.info(f"Reading WizuAll source file: {args.source_file}")
        with open(args.source_file, 'r') as f:
            source_code = f.read()
        
        # Process data file if provided
        if args.data:
            if not os.path.exists(args.data):
                logger.error(f"Data file not found: {args.data}")
                return 1
            
            logger.info(f"Processing data file: {args.data}")
            if args.data.lower().endswith('.pdf'):
                extractor = PDFExtractor(args.data)
                data = extractor.extract_numeric_data()
                formatter = DataFormatter(data)
                data_stream = formatter.to_stream()
                logger.info(f"Extracted {len(data)} numeric values from PDF")
            else:
                # Assume it's a CSV or raw data file
                with open(args.data, 'r') as f:
                    data_stream = f.read()
            
            # Here we would inject the data into the source code or pass it to the compiler
            # For now, we'll just log it
            logger.debug(f"Data stream:\n{data_stream[:100]}...")
        
        # Lexical analysis
        logger.info("Performing lexical analysis...")
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        logger.debug(f"Generated {len(tokens)} tokens")
        
        # Syntax analysis
        logger.info("Parsing source code...")
        parser = Parser(tokens)
        ast = parser.parse()
        logger.info("Parsing completed successfully")
        
        # Semantic analysis
        logger.info("Performing semantic analysis...")
        semantic_analyzer = SemanticAnalyzer(ast)
        valid, errors = semantic_analyzer.analyze()
        
        if not valid:
            for error in errors:
                logger.error(f"Semantic error: {error}")
            return 1
        
        logger.info("Semantic analysis completed successfully")
        
        # Code generation
        logger.info(f"Generating {args.target} code...")
        code_generator = CodeGenerator(ast, args.target)
        target_code = code_generator.generate()
        
        # Output the generated code
        if args.output:
            with open(args.output, 'w') as f:
                f.write(target_code)
            logger.info(f"Generated code saved to: {args.output}")
        else:
            # Default output filename based on input and target language
            base_name = os.path.splitext(args.source_file)[0]
            extensions = {'python': '.py', 'c': '.c', 'r': '.R'}
            output_file = f"{base_name}{extensions.get(args.target, '.txt')}"
            
            with open(output_file, 'w') as f:
                f.write(target_code)
            logger.info(f"Generated code saved to: {output_file}")
        
        # Execute the generated code if requested
        if args.execute:
            logger.info(f"Executing generated {args.target} code...")
            executor = RuntimeExecutor(target_code, args.target)
            
            try:
                output = executor.execute()
                logger.info("Execution completed successfully")
                logger.info("Output:")
                print(output)
            except Exception as e:
                logger.error(f"Execution error: {str(e)}")
                return 1
        
        logger.info("WizuAll compilation completed successfully")
        return 0
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if args.verbose:
            logger.exception("Detailed traceback:")
        return 1

if __name__ == "__main__":
    sys.exit(main())