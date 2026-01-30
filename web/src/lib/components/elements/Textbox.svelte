<script lang="ts">
  interface Props {
    type?: string;
    name?: string;
    placeholder?: string;
    disabled?: boolean;
    width?: string;
    value?: string;
    autocomplete?: string | undefined;
    required?: boolean;
  }

  let {
    type = 'text',
    name = 'text',
    placeholder = '',
    disabled = false,
    width = '100%',
    value = $bindable(''),
    autocomplete = undefined,
    required = false
  }: Props = $props();
</script>


{#if type === 'password'}
  <input
    {name}
    type="password"
    bind:value
    {placeholder}
    {autocomplete}
    style:width={width}
    {disabled}
    {required}
  />
{:else if type === 'email'}
  <input
    {name}
    type="email"
    bind:value
    {placeholder}
    {autocomplete}
    style:width={width}
    {disabled}
    {required}
  />
{:else}
  <input
    {name}
    type="text"
    bind:value
    {placeholder}
    {autocomplete}
    style:width={width}
    {disabled}
    {required}
  />
{/if}


<style>
  input {
    display: block;
    padding: 12px;
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    border-radius: var(--radius-m);
    color: var(--dark-text);
    font-family: var(--font-family);
    transition: all 0.2s ease;
    backdrop-filter: blur(32px);
  }
</style>
