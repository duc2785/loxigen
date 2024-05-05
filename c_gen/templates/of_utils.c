:: # Copyright 2013, Big Switch Networks, Inc.
:: #
:: # LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
:: # the following special exception:
:: #
:: # LOXI Exception
:: #
:: # As a special exception to the terms of the EPL, you may distribute libraries
:: # generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
:: # that copyright and licensing notices generated by LoxiGen are not altered or removed
:: # from the LoxiGen Libraries and the notice provided below is (i) included in
:: # the LoxiGen Libraries, if distributed in source code form and (ii) included in any
:: # documentation for the LoxiGen Libraries, if distributed in binary form.
:: #
:: # Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
:: #
:: # You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
:: # a copy of the EPL at:
:: #
:: # http://www.eclipse.org/legal/epl-v10.html
:: #
:: # Unless required by applicable law or agreed to in writing, software
:: # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
:: # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
:: # EPL for the specific language governing permissions and limitations
:: # under the EPL.
::
:: include('_copyright.c')

/****************************************************************
 * File: of_utils.h
 *
 * Some utilities provided based on LOCI code generation
 *
 ****************************************************************/

#include <loci/of_utils.h>
#include <stdio.h>
#include <stdlib.h>


/**
 * Check if the given port is used as an output for any entry on the list
 * @param actions The list of actions being checked
 * @param outport The port being sought
 * @returns Boolean, true if entry has an output action to outport
 *
 * @fixme VERSION Currently only OF 1.0 supported
 * @fixme Check for error return in accessor
 *
 * If outport is "wildcard", the test should be ignored, so return true
 */

int
of_action_list_has_out_port(of_list_action_t *actions, of_port_no_t outport)
{
    of_object_t elt;
    of_action_output_t *output;
    int loop_rv;
    of_port_no_t port_no;
    int rv = 0;

    if (outport == OF_PORT_DEST_WILDCARD) { /* Same as OFPP_ANY */
        return 1;
    }

    output = &elt;
    OF_LIST_ACTION_ITER(actions, &elt, loop_rv) {
        if (output->object_id == OF_ACTION_OUTPUT) {
            of_action_output_port_get(output, &port_no);
            if (port_no == outport) {
                rv = 1;
                break;
            }
        }
    }

    return rv;
}

void
loci_assert_fail(const char *msg, const char *file, unsigned int line)
{
    fprintf(stderr, "\\nASSERT %s. %s:%d\\n", msg, file, line);
    abort();
}
