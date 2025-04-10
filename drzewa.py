#!/usr/bin/env python3
import sys
import argparse


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


def insert_bst(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert_bst(root.left, value)
    else:
        root.right = insert_bst(root.right, value)
    return root


def insert_avl(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert_avl(root.left, value)
    else:
        root.right = insert_avl(root.right, value)

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1 and value < root.left.value:
        return right_rotate(root)
    if balance < -1 and value > root.right.value:
        return left_rotate(root)
    if balance > 1 and value > root.left.value:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1 and value < root.right.value:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root


def left_rotate(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x


def get_height(root):
    if root is None:
        return 0
    return root.height


def get_balance(root):
    if root is None:
        return 0
    return get_height(root.left) - get_height(root.right)


def print_inorder(root):
    return print_tree(root, 'inorder')


def print_preorder(root):
    return print_tree(root, 'preorder')


def print_postorder(root):
    return print_tree(root, 'postorder')


def print_tree(root, order):
    result = []
    if root:
        if order == 'preorder':
            result.append(root.value)
        result.extend(print_tree(root.left, order))
        if order == 'inorder':
            result.append(root.value)
        result.extend(print_tree(root.right, order))
        if order == 'postorder':
            result.append(root.value)
    return result


def find_min(root):
    while root and root.left:
        root = root.left
    return root


def find_max(root):
    while root and root.right:
        root = root.right
    return root


def remove(root, value):
    if root is None:
        return root

    if value < root.value:
        root.left = remove(root.left, value)
    elif value > root.value:
        root.right = remove(root.right, value)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        else:
            min_larger_node = find_min(root.right)
            root.value = min_larger_node.value
            root.right = remove(root.right, min_larger_node.value)
    return root


def delete_tree(root):
    if root:
        root.left = delete_tree(root.left)
        root.right = delete_tree(root.right)
        root = None
    return root


def rebalance_tree(root, insert_values):
    root = None
    for value in insert_values:
        root = insert_avl(root, value)
    return root


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", choices=["AVL", "BST"], required=True)
    args = parser.parse_args()

    input_line = input("values> ").strip()
    values = list(map(int, input_line.split()))

    num_nodes = values[0]  # liczba węzłów
    insert_values = values[1:num_nodes+1]  # same wartości do wstawienia

    print(f"nodes> {num_nodes}")
    print(f"insert> {' '.join(map(str, insert_values))}")
    if args.tree == "AVL":
        print("Sorted:", ', '.join(map(str, sorted(insert_values))))
        n = len(insert_values)
        if n % 2 == 0:
            median = (sorted(insert_values)[n//2 - 1] + sorted(insert_values)[n//2]) / 2
        else:
            median = sorted(insert_values)[n//2]
        print("Median:", median)
    else:
        print(f"Inserting: {', '.join(map(str, insert_values))}")
    print("Type 'Help' for list of commands.")

    root = None
    if args.tree == "AVL":
        for value in insert_values:
            root = insert_avl(root, value)
    else:  # Drzewo BST
        for value in insert_values:
            root = insert_bst(root, value)

    while True:
        try:
            action = input("action> ").strip().lower()
        except EOFError:
            print("Program exited with status: 0")
            break

        if action == "help":
            print("Help - Show this message")
            print("Print - Print the tree usin In-order, Pre-order, Post-order")
            print("Remove - Remove elements of the tree")
            print("Delete - Delete whole tree")
            print("Export - Export the tree to tickzpicture")
            print("Rebalance - Rebalance the tree")
            print("Exit - Exits the program (same as ctrl+D)")
        elif action == "print":
            print("In-order:", ', '.join(map(str, print_inorder(root))))
            print("Pre-order:", ', '.join(map(str, print_preorder(root))))
            print("Post-order:", ', '.join(map(str, print_postorder(root))))
        elif action == "findminmax":
            if root:
                min_node = find_min(root)
                max_node = find_max(root)
                print(f"Min: {min_node.value}")
                print(f"Max: {max_node.value}")
            else:
                print("Tree is empty.")
        elif action == "remove":
            to_remove = input("remove> ").strip().split()
            for val in map(int, to_remove):
                root = remove(root, val)
        elif action == "delete":
            root = delete_tree(root)
        elif action == "delete all":
            root = delete_tree(root)
            print("Tree successfully removed")
        elif action == "rebalance":
            root = rebalance_tree(root, insert_values)
        elif action.lower() == "export":
            tikz_code = export_to_tikzpicture(root)
            print("TikZ output:\n")
            print(tikz_code)

        elif action == "exit":
            print("Program exited with status: 0")
            break
        else:
            print("Unknown command.")


def export_to_tikzpicture(root):
    def tikz_node(node):
        if node is None:
            return ""
        left = tikz_node(node.left)
        right = tikz_node(node.right)
        s = f"[.{node.value}"
        if node.left:
            s += f" {left}"
        else:
            s += " [.$\\varnothing$ ]"
        if node.right:
            s += f" {right}"
        else:
            s += " [.$\\varnothing$ ]"
        s += "]"
        return s

    tikz_code = "\\begin{tikzpicture}[sibling distance=10em, level distance=4em,\n"
    tikz_code += "every node/.style = {shape=circle, draw, align=center}]\n"
    tikz_code += "\\Tree " + tikz_node(root) + "\n"
    tikz_code += "\\end{tikzpicture}"
    return tikz_code


if __name__ == "__main__":
    main()
