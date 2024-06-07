import os


def scan_vmt_files(location):
    vmt_files = []
    for root, dirs, files in os.walk(location):
        for file in files:
            if file.endswith(".vmt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as vmt_file:
                    lines = vmt_file.readlines()
                    if lines:
                        vmt_files.append((file_path, lines))
    return vmt_files


def format_vmt_file(file_path, lines):
    formatted_lines = []
    current_block = []
    in_block = False
    shader_name = None
    original_shader_comment = None

    for line in lines:
        line = line.strip()
        if line.startswith("//"):
            if "original shader:" in line:
                original_shader_comment = line
            else:
                formatted_lines.append(line)
        elif line.startswith('"') and line.endswith('"'):
            if in_block:
                current_block.append(line)
            else:
                if not shader_name:
                    shader_name = line
                    formatted_lines.append(shader_name + " {")
        elif line.startswith("{"):
            in_block = True
        elif line.startswith("}"):
            current_block.append(line)
            formatted_lines.extend(format_block(original_shader_comment, current_block))
            current_block = []
            in_block = False
            shader_name = None
            original_shader_comment = None
        elif in_block:
            current_block.append(line)

    formatted_lines = [line for line in formatted_lines if line.strip()]

    with open(file_path, "w") as vmt_file:
        vmt_file.write("\n".join(formatted_lines))


def format_block(original_shader_comment, block):
    formatted_block = []
    if original_shader_comment:
        formatted_block.append("\t" + original_shader_comment.strip() + "\n")
    for line in block:
        if line.startswith("{"):
            continue
        elif line.startswith("}"):
            formatted_block.append("}\n")
        else:
            formatted_block.append("\t" + line.strip() + "\n")
    return formatted_block


if __name__ == "__main__":
    location = input("Enter the location to scan: ")
    vmt_files = scan_vmt_files(location)

    if vmt_files:
        for file_path, _ in vmt_files:
            print(f"File: {file_path}")

        format_files = input("Do you want to format all files? (y/n) ").lower() == "y"
        if format_files:
            for file_path, lines in vmt_files:
                format_vmt_file(file_path, lines)
    else:
        print("No .vmt files found in the specified location.")
