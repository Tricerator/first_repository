#!/usr/bin/env python3

import math


class ABNode:
    """Single node in an ABTree.

    Each node contains keys and childrens
    (with one more children than there are keys).
    """

    def __init__(self, keys=None, children=None):
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []

    def find_branch(self, key):
        """ Try finding given key in this node.

        If this node contains the given key, returns (True, key_position).
        If not, returns (False, first_position_with_key_greater_than_the_given).
        """
        i = 0
        while (i < len(self.keys) and self.keys[i] < key):
            i += 1

        return i < len(self.keys) and self.keys[i] == key, i

    def insert_branch(self, i, key, child):
        """ Insert a new key and a given child between keys i and i+1."""
        self.keys.insert(i, key)
        self.children.insert(i + 1, child)


class ABTree:
    """A class representing the whole ABTree."""

    def __init__(self, a, b):
        assert a >= 2 and b >= 2 * a - 1, "Invalid values of a, b: {}, {}".format(a, b)
        self.a = a
        self.b = b
        self.root = ABNode(children=[None])

    def find(self, key):
        """Find a key in the tree.

        Returns True if the key is present, False otherwise.
        """
        node = self.root
        while node:
            found, i = node.find_branch(key)
            if found: return True
            node = node.children[i]
        return False

    def insertRecursive(self, subRoot, key, left, right, middle):
        # Jsem v listu
        if subRoot is None:
            return key, None, None

        # Jestlize je hodnota pritomna, nedelej nic

        result = False
        position = 0
        result, position = subRoot.find_branch(key)

        if result:
            return None, None, None
        myNewNode = subRoot.children[position]
        middle, left, right = self.insertRecursive(myNewNode, key, left, right, middle)

        if middle is None:
            return None, left, right

        elif left is None and right is None:
            subRoot.insert_branch(position, key, None)
        else:
            subRoot.insert_branch(position, middle, right)

        if len(subRoot.keys) == self.b:
            indexSplit = int((self.b - 1) / 2)
            middle = subRoot.keys[indexSplit]

            right = ABNode()
            for i in range(indexSplit + 1, len(subRoot.keys) - 1):
                right.keys.append(subRoot.keys[i])
            for i in range(indexSplit + 1, len(subRoot.children) - 1):
                right.children.append(subRoot.children[i])

            for i in range(len(subRoot.keys) - 1, indexSplit + 1):
                del (subRoot.keys[i])
            for i in range(len(subRoot.children) - 1, indexSplit + 1):
                del (subRoot.children[i])

            left = subRoot
        else:
            left = None
            right = None
            middle = None

        return middle, left, right

    def insert(self, key):
        """Add a given key to the tree, unless already present."""
        left = None
        right = None
        value = None

        if self.root is None:
            self.root = ABNode()
            self.root.append(key)
            return
        value, left, right = self.insertRecursive(self.root, key, left, right, value)

        if right is not None:
            newRoot = ABNode()
            newRoot.children.append(left)
            newRoot.children.append(right)
            newRoot.children.append(value)
            self.root = newRoot
