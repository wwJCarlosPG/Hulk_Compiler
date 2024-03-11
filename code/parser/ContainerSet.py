class ContainerSet:
    """
    ContainerSet is a class representing a set with an optional epsilon element.

    Parameters:
        *values: Values to initialize the set with.
        contains_epsilon (bool): Indicates whether the set contains an epsilon element. Default is False.
    """

    def __init__(self, *values, contains_epsilon=False):
        """
        Initialize ContainerSet with values and epsilon status.

        Args:
            *values: Values to initialize the set with.
            contains_epsilon (bool): Indicates whether the set contains an epsilon element. Default is False.
        """
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value):
        """
        Add a value to the set.

        Args:
            value: Value to be added to the set.

        Returns:
            bool: True if the set was modified, False otherwise.
        """
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def set_epsilon(self, value=True):
        """
        Set the epsilon status of the set.

        Args:
            value (bool): New epsilon status.

        Returns:
            bool: True if the epsilon status was modified, False otherwise.
        """
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    def update(self, other):
        """
        Update the set with the elements from another set.

        Args:
            other (ContainerSet): Another ContainerSet.

        Returns:
            bool: True if the set was modified, False otherwise.
        """
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other):
        """
        Update the epsilon status based on another set.

        Args:
            other (ContainerSet): Another ContainerSet.

        Returns:
            bool: True if the epsilon status was modified, False otherwise.
        """
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)

    def hard_update(self, other):
        """
        Perform a hard update, combining both element and epsilon updates.

        Args:
            other (ContainerSet): Another ContainerSet.

        Returns:
            bool: True if either the set or epsilon status was modified, False otherwise.
        """
        return self.update(other) | self.epsilon_update(other)

    def __len__(self):
        """
        Get the length of the set.

        Returns:
            int: Number of elements in the set.
        """
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        """
        Get a string representation of the ContainerSet.

        Returns:
            str: String representation of the set.
        """
        return f'{str(self.set)}-{self.contains_epsilon}'

    def __repr__(self):
        """
        Get a string representation of the ContainerSet for debugging.

        Returns:
            str: String representation of the set.
        """
        return str(self)

    def __iter__(self):
        """
        Get an iterator for the set.

        Returns:
            iter: Iterator for the set.
        """
        return iter(self.set)

    def __eq__(self, other):
        """
        Check if two ContainerSets are equal.

        Args:
            other (ContainerSet): Another ContainerSet.

        Returns:
            bool: True if both sets and epsilon statuses are equal, False otherwise.
        """
        return isinstance(other, ContainerSet) and self.set == other.set and self.contains_epsilon == other.contains_epsilon
    
    def __contains__(self, value):
        """
        Check if a value is present in the set.

        Args:
            value: Value to check for membership.

        Returns:
            bool: True if the value is present in the set, considering epsilon if applicable, False otherwise.
        """
        return value in self.set or (self.contains_epsilon and not self.set)

    def __and__(self, other):
        """
        Compute the intersection of two ContainerSets.

        Args:
            other (ContainerSet): Another ContainerSet.

        Returns:
            ContainerSet: A new ContainerSet representing the intersection of the two sets.
        """
        intersection_set = self.set.intersection(other.set)
        intersection_epsilon = self.contains_epsilon and other.contains_epsilon
        return ContainerSet(*intersection_set, contains_epsilon=intersection_epsilon)

    def __or__(self, other):
        """
        Compute the union of two ContainerSets.

        Args:
            other (ContainerSet): Another ContainerSet.

        Returns:
            ContainerSet: A new ContainerSet representing the union of the two sets.
        """
        union_set = self.set.union(other.set)
        union_epsilon = self.contains_epsilon or other.contains_epsilon
        return ContainerSet(*union_set, contains_epsilon=union_epsilon)

    def __sub__(self, other):
        """
        Compute the set difference of two ContainerSets.

        Args:
            other (ContainerSet): Another ContainerSet.

        Returns:
            ContainerSet: A new ContainerSet representing the set difference (self - other).
        """
        difference_set = self.set.difference(other.set)
        difference_epsilon = self.contains_epsilon and not other.contains_epsilon
        return ContainerSet(*difference_set, contains_epsilon=difference_epsilon)

    def __xor__(self, other):
        """
        Compute the symmetric difference of two ContainerSets.

        Args:
            other (ContainerSet): Another ContainerSet.

        Returns:
            ContainerSet: A new ContainerSet representing the symmetric difference of the two sets.
        """
        symmetric_difference_set = self.set.symmetric_difference(other.set)
        symmetric_difference_epsilon = (self.contains_epsilon and not other.contains_epsilon) or (
            not self.contains_epsilon and other.contains_epsilon
        )
        return ContainerSet(*symmetric_difference_set, contains_epsilon=symmetric_difference_epsilon)
